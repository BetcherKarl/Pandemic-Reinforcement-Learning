

class Logger:
    def __init__(self, name: str):
        self.name = name
        self.path = './logs/' + name + '.log'

    def log(self, message: str):
        with open(path, 'a') as f:
            f.write(message + '\n')