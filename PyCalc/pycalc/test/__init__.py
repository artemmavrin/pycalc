def ConsoleTest(function):
    def new_function():
        prompt = '> '
        quit_command = 'quit'
        
        print("Type '" + quit_command + "' to exit the program.")
        
        while True:
            line = input(prompt)
            if line == quit_command:
                break
            elif line:
                try:
                    function(line)
                except Exception:
                    print('There was an error.')
    
    return new_function