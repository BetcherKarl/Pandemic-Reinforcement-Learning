from colorama import Fore, Back, Style

class Logger:
    def __init__(self, name: str):
        self.name = name
        self.path = './logs/' + name + '.log'

    def print(self, message: str):
        with open(self.path, 'a') as f:
            f.write(message + '\n')
        print(message)

    def warn(self, message: str):
        with open(self.path, 'a'):
            f.write('WARNING: ' + message + '\n\n')
        print(f"{Fore.RED}{message}{Style.RESET_ALL}")
