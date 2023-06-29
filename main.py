from pprint import pprint

import requests
from bs4 import BeautifulSoup
import argparse
import time
import subprocess
import os

url = "http://83.151.134.6/Status.asp"
global data
global html
parser = argparse.ArgumentParser(description="Show washing machine status")

parser.add_argument('machine_num', type=int, nargs='?', help='Specify machine number to filter. example: "1" for A1')
parser.add_argument('-f', action='store_true', dest='follow', help='Use "-f" flag to ring terminal bell when active machine is finished')
args = parser.parse_args()

def getmachine_data():
    data = requests.get(url)
    html = BeautifulSoup(data.text, "html.parser")
    machine_data = html.select('TD.noborder')
    length = len(machine_data)
    machine_data = machine_data[2:]
    return machine_data

def getmachineinfo(opt_pos_arg: int, arr: []):

    if opt_pos_arg > 0 and opt_pos_arg < 9:
        match opt_pos_arg:
            case 7:
                return arr[0]

            case 8:
                return arr[1]

            case _:
                return arr[opt_pos_arg +1]
        
    else:
        return "No machine with number %d" % opt_pos_arg


def ansiprint(string: str):
    string = string.replace("Fri", " \033[32mFri\033[0m")
    string = string.replace("Optaget", " \033[31mOptaget\033[0m")
    string = string.replace("Res.", " \033[33mRes.\033[0m")
    string = string.replace("Lukket", " \033[31mLukket\033[0m") 
    print(string)

def getparsed_arr():
    machine_data = getmachine_data() 
    arr = []
    i = 0
    s = ""

    for d in machine_data:
        if i >= 5:
            arr.append(s)
            i = 0
            s = ""

        s += d.text.replace("\xa0", " ")
        i += 1

    del arr[len(arr) - 2:]
    return arr

def ring_bell(termux: bool, num: int):
    if termux:
        os.popen(f'termux-notification -t "Machine {num} has finished" --vibrate 500')

    else:
        finished = False
        count = 0
        last_time = time.thread_time()
        while not finished:
            time_diff = time.thread_time() - last_time
            if (time_diff >= 1):
                print('\a')
                count += 1
                last_time = time.thread_time()
                if (count >= 3):
                    finished = True



arr = getparsed_arr()

# Check if running in termux environment
termux = False
res = os.popen('command -v termux-setup-storage')

if (len(res.read()) > 0):
   termux = True
res.close()


# Run branch based on arguments
if args.machine_num is not None and args.follow == False:
    ansiprint(getmachineinfo(args.machine_num, arr))

elif args.machine_num is not None and args.follow == True:
    info = getmachineinfo(args.machine_num, arr)

    if (info.count("Fri") > 0 or info.count("Lukket") > 0):
        print("Cannot follow. Machine not in use!")

    else:
        print(f'Following machine {args.machine_num}')
        finished = False
        last_time = time.thread_time()
        while not finished:
            time_diff = time.thread_time() - last_time
            if time_diff < 60:
                continue
            
            else:
                arr = getparsed_arr()
                info = getmachineinfo(args.machine_num, arr)
                last_time = time.thread_time()

                if info.count("Fri") > 0:
                    ansiprint(info)
                    ring_bell(termux, args.machine_num)
                    finished = True

elif args.machine_num is None and args.follow == True:
    print("No machine specified to follow!")

else:
    for x in arr:
        ansiprint(x)
        