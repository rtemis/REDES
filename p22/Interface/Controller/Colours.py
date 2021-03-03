"""
 File: Colours.py
 Authors: Leah Hadeed
          Nazariy Gunko

 Description:
 This script adds colour to the terminal output.

"""

# This class, when defined, allows a user to change the terminal output text colour.
class Colours:

    # Change colour: RED
    def red(self, string):
        return '\x1b[1;31m' + string + '\x1b[0m'

    # Change colour: GREEN
    def green(self, string):
        return '\x1b[1;32m' + string + '\x1b[0m'
    
    # Change colour: YELLOW
    def yellow(self, string):
        return '\x1b[1;33m' + string + '\x1b[0m'

    # Change colour: BLUE
    def blue(self, string):
        return '\x1b[1;34m' + string + '\x1b[0m'

    # Change colour: MAGENTA
    def magenta(self, string):
        return '\x1b[1;35m' + string + '\x1b[0m'

    # Change colour: CYAN
    def cyan(self, string):
        return '\x1b[1;36m' + string + '\x1b[0m'

    # Test colour output
    def test():
        c = Colours()
        
        print(c.red('Structure Error: ') + "python3 securebox_client.py " + c.magenta('--create_id <name> <email> OPTIONAL <alias>'))

        print('Hello ' + c.green('World'))
        print(c.red('ERROR'))
        print('This is ' + c.magenta('MAGENTA'))
