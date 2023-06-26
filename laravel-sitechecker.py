#!/usr/bin/env python3
# Mass Laravel Site Checker
# Created By Im-Hanzou
# Using threading for multi-worker
# Usage: python laravel-sitechecker.py list.txt thread

import sys
import threading
import requests
import urllib3
from colorama import Fore, Style
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print(Fore.CYAN + r"""
  _                                _ 
 | |    __ _  _ _  __ _ __ __ ___ | |
 | |__ / _` || '_|/ _` |\ V // -_)| |
 |____|\__,_||_|  \__,_| \_/ \___||_|
                                     
""")
print(Fore.YELLOW + "Mass Laravel Site Checker\nGithub: im-hanzou\nUsage: python laravel-sitechecker.py list.txt thread\nExample: python laravel-sitechecker.py list.txt 50\n\n")
Style.RESET_ALL

def exploit(target):
    classic = Style.RESET_ALL
    try:
        result = requests.get(target, timeout=10, verify=False)
        if 'XSRF-TOKEN' in result.cookies or '_session' in result.cookies:
            print(Fore.GREEN + "[ Valid ]" + classic + " => [ " + target + " | Laravel Site ]")
            with open('laravel.txt', 'a') as f:
                f.write(target + '\n')
        else:
            print(Fore.RED + "[ Not Valid ]" + classic + " => " + target)
            with open('notlaravel.txt', 'a') as f:
                f.write(target + '\n')
    except requests.exceptions.Timeout:
        print(Fore.RED + "[ Timeout ]" + classic + " => " + target)
    except requests.exceptions.RequestException:
        print(Fore.RED + "[ Connection Error ]" + classic + " => " + target)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python laravel-sitechecker.py list.txt thread")
        sys.exit(1)

    target_file = sys.argv[1]
    num_threads = int(sys.argv[2])

    targets = []
    with open(target_file, 'r') as f:
        targets = f.read().splitlines()

    threads = []
    for target in targets:
        t = threading.Thread(target=exploit, args=(target,))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

laravel_file = 'laravel.txt'
notlaravel_file = 'notlaravel.txt'

with open(laravel_file, 'r') as f:
    laravel_lines = len(f.readlines())

with open(notlaravel_file, 'r') as f:
    notlaravel_lines = len(f.readlines())

print(Fore.CYAN + f"Laravel Site: {laravel_file} ({laravel_lines} Sites)")
print(Fore.CYAN + f"Not Laravel Site: {notlaravel_file} ({notlaravel_lines} Sites)")
