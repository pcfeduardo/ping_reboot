#!/usr/bin/env python
import subprocess
from datetime import datetime
import time
import os
import sys
fail_count = 0

# You can change it
hostname1 = "8.8.8.8"
hostname2 = "1.1.1.1"
sleep_time = 5
max_failure = 10

class style():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
restore_connection = ['reboot']

if sys.version_info.major < 3:
    print('You need python version 3 or higher!')
    sys.exit(0)

if os.geteuid() != 0:
    print(f'{style.FAIL}Sorry, the script only works as root! :({style.ENDC}')
    sys.exit(1)

def healthcheck(hostname):
    return ['ping', hostname, '-c', '1', '-t', '3']

print(f'{style.HEADER}==============================================')
print(f'Started at: {datetime.now()}{style.ENDC}\n')

while True:
    check1 = subprocess.run(healthcheck(hostname1), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check1.returncode == 0:
        fail_count = 0
        print(f'{style.OKGREEN}[*] {datetime.now()} - {hostname1} is up!{style.ENDC}')
    else:
        check2 = subprocess.run(healthcheck(hostname2), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check2.returncode > 0:
            print(f'{style.WARNING}[*] {datetime.now()} - {hostname1} and {hostname2} are down!{style.ENDC}')
            fail_count = fail_count + 1
    if fail_count == max_failure:
        print(f'{style.FAIL}[*] {datetime.now()} - Maximum failures have been reached at {max_failure}. Trying to recover the connection{style.ENDC}')
        recover = subprocess.run(restore_connection, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if recover.returncode != 0:
            print(f'{style.FAIL}[*] {datetime.now()} - Error: {recover.stderr}')
        else:
            print(f'{style.OKCYAN}[*] {datetime.now()} - Success... {recover.stdout}')
    time.sleep(sleep_time)
