import subprocess as s
import threading
import json
import commands
import msvcrt
import wmi
import os
import argparse
import sys



def clear():
    os.system('cls')

def print_dict(dict):
    for key in dict:
        print(50* '-' + '\n' + key + '\n')
        print(dict[key])

def HandleCredentials(credentials):
    user,password = credentials.split(':')
    return user, password

hardware = {
    'BATTERY':commands.battery_wmi,
    'CPU':commands.cpu_wmi,
    'GPU':commands.gpu_wmi,
    'DISK':commands.disk_wmi,
    'MONITOR':commands.monitor_wmi,
    'RAM':commands.ram_wmi
}

network = {
    'IP':commands.adapters_wmi,
    'ROUTE':commands.route_wmi
}

domain = {

}

BANNER = '''
1. Hardware
2. Network
3. Hide/Show Menu
4. Clear
q. Quit (or q)
'''



if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=True, description="Administrator WMI Assistant - helps you manage your computers locally and remotely")
    parser.add_argument('-target', action='store', default='.', help='AdminRookie.exe <computer_name> - run the program for remote machine')
    parser.add_argument('-hardware', action='store_true', help="Display hardware information, don't run menu")
    parser.add_argument('-network', action='store_true', help="Display network information, don't run menu")
    group = parser.add_argument_group('authentication')
    group.add_argument('-credentials', action="store", metavar="USERNAME:PASSWORD", help='Supply username and password')
   
    options = parser.parse_args()
    
    #Credentials handle

    if options.credentials != None:
        user, password = HandleCredentials(options.credentials)
    else:
        user,password = '', ''
    #load data before running the program.
    thread = []


    if options.hardware:
        for key in hardware:
            thread.append(threading.Thread(target=hardware[key], args=(key,hardware, options.target, password, user)))
        for x in range(0, len(thread)):
            thread[x].start()
        for x in range(0, len(thread)):
            thread[x].join()
        print_dict(hardware)
        input('Press ENTER to exit')
        sys.exit(0)

    if options.network:
        for key in network:
            thread.append(threading.Thread(target=network[key], args=(key,network, options.target, password, user,)))
        for x in range(0, len(thread)):
            thread[x].start()
        for x in range(0, len(thread)):
            thread[x].join()
        print_dict(network)
        input('Press ENTER to exit')
        sys.exit(0)

    # Load information before displaying menu

    for key in network:
        thread.append(threading.Thread(target=network[key], args=(key, network,options.target,password, user)))
    for key in hardware:
        thread.append(threading.Thread(target=hardware[key], args=(key,hardware,options.target, password, user)))
    
    for x in range(0, len(thread)):
        thread[x].start()

    for x in range(0, len(thread)):
        thread[x].join()

    #MENU OPTIONS
    hide = False
    while(True):
        if hide == False:
            print(BANNER)
        choice = msvcrt.getch().decode()
        match choice:
            case '1':
                clear()
                print_dict(hardware)
            case '2':
                clear()
                print_dict(network)
            case '3':
                clear()
                print('Menu toggled')
                hide = not hide
            case '4':
                clear()
            case 'q':
                print('Quiting...')
                sys.exit(0)