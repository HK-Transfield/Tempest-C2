import socket
import sys

def listener_handler():
    """
    This function hosts the listener for the socket, binds the socket, accepts
    traffic, and then redirects that traffic.
    """

    # 1 Accept Connection
    sock.bind((host_ip, host_port))

    print('[+] Awaiting connection from client...')

    sock.listen()
    remote_target, remote_ip = sock.accept()
    comm_handler(remote_target, remote_ip)


def comm_handler(remote_target, remote_ip):
    """
    This function directs traffic to where it needs to go and ensures that it is
    receiving it where needed.
    """
    print(f'[+] Connection received from {remote_ip}')
     # 2 Handle Sending
    while True:
        try:
            message = input('Message to send#>')
            if message == 'exit':
                remote_target.send(message.encode())
                remote_target.close()
                break

            remote_target.send(message.encode())

            # 3 handle receiving
            response = remote_target.recv(1024).decode()

            if response == 'exit':
                print('[-] The client has terminated the session')
                remote_target.close()
                break
            print(response)

        except KeyboardInterrupt:
            print('[-] Keyboard interrupt')
            remote_target.close()
            break

        except Exception:
                remote_target.close()
                break


def comm_in(remote_target):
    """
    This function handles all the responses sent from the sockclient
    back to the sockserver.
    """
    print('[+] Awaiting response...')
    response = remote_target.recv.decode()
    return response

def comm_out(remote_target, message):
    """
    This function sends commands from the sock server to the sockclient.
    """
    remote_target.send(message.encode())


if __name__ == '__main__':
    # generate the socket handler for our code
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = sys.argv[1]
    host_port = int(sys.argv[2])
    listener_handler()
