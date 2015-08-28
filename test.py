class ConsoleTest(object):
    '''Decorator for repeatedly executing a function taking a user input in the
    console.
    '''
    def __init__(self, f):
        self.f = f
        self.prompt = '> '
        self.quit = 'quit'

    def __call__(self):
        print("Type '" + self.quit + "' to exit the program.")

        while True:
            line = input(self.prompt)
            if line == self.quit:
                break
            elif line:
                self.f(line)
