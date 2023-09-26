import socket


def listener_handler():
    # bind the socket to the local address
    sock.bind((host_ip, host_port))

    print('[+] Awaiting connection from client...')

    # listen for incoming connections
    sock.listen()

    # accept connection
    # the value is a pair containing a new socket object
    remote_target, remote_ip = sock.accept()

    print(f'[+] Connection received from {remote_ip}')

    while True:
        try:
            message = input('Message to send#>')
            if message == 'exit':
                remote_target.send(message.encode())
                remote_target.close()
                break

            remote_target.send(message.encode())
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



# generate the socket handler for our code
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip = '127.0.0.1'
host_port = 2222
listener_handler()
