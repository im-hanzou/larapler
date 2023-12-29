import os, requests, time
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool
import threading
import sys
from colorama import Fore, Style


def screen_clear():
    _ = os.system('cls')


bl = Fore.BLUE
wh = Fore.WHITE
gr = Fore.GREEN
red = Fore.RED
res = Style.RESET_ALL
yl = Fore.YELLOW

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'}

def debugbar (star):
    if "://" in star:
      star = star
    else:
      star = "http://" + star
    star = star.replace('\n', '').replace('\r', '')
    url = star + "/"
    check = requests.get(url, headers=headers, timeout=3)
    resp = check.text
    try:
        if "PhpDebugBar.DebugBar" in resp:
            print(f"Debugbar {gr}OK{res} => {star}\n")
            mrigel = open("found.txt", "a")
            mrigel.write(f'{star}/_debugbar/open?method=POST&max=1000&offset=0\n')
        else:
            print(f"{red}Not Found{res} Debugbar => {star}\n")
    except:
        pass


def filter(star):
    try:
       debugbar(star)
    except:
       pass


def main():
    print(f'''{gr}[ DEBUDBAR CHECKER ] | [ BY XNXXVIDOES ]''')
    list = input(f"{gr}Give Me Your List.txt/{red}XNXXVIDOES> {gr}${res} ")
    star = open(list, 'r').readlines()
    try:
       ThreadPool = Pool(50)
       ThreadPool.map(filter, star)
       ThreadPool.close()
       ThreadPool.join()
    except:
       pass
       
if __name__ == '__main__':
    screen_clear()
    main()
