from pprint import pprint

import requests
from bs4 import BeautifulSoup
import argparse
import time

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
    match opt_pos_arg:
        case 7:
            return arr[0]

        case 8:
            return arr[1]

        case 1:
            return arr[2]

        case 2:
            return arr[3]

        case 3:
            return arr[4]

        case 4:
            return arr[5]

        case 5:
            return arr[6]

        case 6:
            return arr[7]


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

arr = getparsed_arr()

if args.machine_num is not None and args.follow == False:
    ansiprint(getmachineinfo(args.machine_num, arr))

elif args.machine_num is not None and args.follow == True:
    info = getmachineinfo(args.machine_num, arr)

    if (info.count("Fri") > 0 or info.count("Lukket") > 0):
        print("Cannot follow. Machine not in use!")

    else:
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
                    print('\a')
                    finished = True


elif args.machine_num is None and args.follow == True:
    print("No machine specified to follow!")

else:
    for x in arr:
        ansiprint(x)
