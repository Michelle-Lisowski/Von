"""
The MIT License (MIT)

Copyright (c) 2018 sirtezza451

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import print_function
import json
import os
import subprocess

INTRO = ('=============\n'
         'Procbot Setup\n'
         '=============\n')
print(INTRO)

def user_input():
    return input('> ')

with open('settings.json', 'r') as fp:
    settings = json.load(fp)

def main():
    if not str('DISCORD_TOKEN') in settings:
        print('Please enter your token from Discord below. '
              'You will not need to do this every time you '
              'run Procbot; this is just first time setup.')
        token = user_input()

        try:
            settings['DISCORD_TOKEN'] = str(token)
            with open('settings.json', 'w') as fp:
                json.dump(settings, fp, indent=4)
        except:
            print('An error occurred. Aborting setup...')
            os.system('exit')
        else:
            print('Your token has been successfully set. Running Procbot...')
            subprocess.call('python main.py')
    else:
        print('Please choose an option below using the corresponding number:')
        print('1. Run Procbot')
        print('2. Update Procbot from master branch')
        print('3. Update Procbot from development branch')
        print('4. Quit')
        choice = user_input()
        if choice == '1':
            try:
                subprocess.call('python main.py')
            except:
                print('An error occurred while running Procbot. Aborting setup...')
                os.system('exit')
        elif choice == '2':
            try:
                subprocess.call('git pull . master')
            except:
                print('An error occurred while updating Procbot. Make sure Git is'
                      'installed AND added to the PATH environment variable.')
            else:
                print('Procbot has been successfully updated.')
        elif choice == '3':
            try:
                subprocess.call('git pull . development')
            except:
                print('An error occurred while updating Procbot. Make sure Git is'
                      'installed AND added to the PATH environment variable.')
            else:
                print('Procbot has been successfully updated.')
        elif choice == '4':
            os.system('exit')

if __name__ == '__main__':
    main()
