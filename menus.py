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
    print(bcolors.HEADER + '  \_/  \____\\\\_/  \|\_/   \____\\\\____/  \_/ ' + bcolors.ENDC)
    print(bcolors.HEADER + bcolors.BOLD + '\nCreated By HK Transfield' + bcolors.ENDC)
    print(bcolors.HEADER + '=============================================\n' + bcolors.ENDC)

def help():
    print('''

    Menu Commands
    ----------------------------------------------------------------------------------------
    listeners -g            ---> Generate a new listener
    winplant py             ---> Generate a Windows compatible Python payload
    unixplant py            ---> Generate a Linux compatible Python payload
    exeplant                ---> Generate an executable payload for windows
    sessions -l             ---> List sessions
    sessions -i <id>        ---> Interact with a new sessions
    kill <id>               ---> Kills an active session

    Session Commands
    ----------------------------------------------------------------------------------------
    background              ---> Backgrounds the current session
    exit                    ---> Terminates the current session
    ''')
