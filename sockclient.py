import socket


def session_handler():
    print(f'[+] Connecting to {tar_ip}')
    sock.connect((tar_ip, tar_port))
    print(f'[+] Connected to {tar_ip}')

    while True:
        try:
            print('[+] Awaiting response...')
            message = sock.recv(1024).decode()

            if message == 'exit':
                print('[-] The server has terminated the session')
                sock.close()
                break

            print(message)

            response = input('Message to send#>')

            if response == 'exit':
                sock.send(response.endcode())
                sock.close()
                break

            sock.send(response.encode())

        except KeyboardInterrupt:
            print('[-] Keyboard interrupt')
            sock.close()
            break

        except Exception:
            sock.close()
            break


# generate the socket handler for our code
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# target host
tar_ip = '127.0.0.1'
tar_port = 2222
session_handler()
