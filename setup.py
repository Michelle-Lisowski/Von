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

INTRO = ('===========\n'
         'Jaffa Setup\n'
         '===========\n')
print(INTRO)

def user_input():
    return input('> ')

with open('settings.json', 'r') as fp:
    settings = json.load(fp)

def main():
    if not str('DISCORD_TOKEN') in settings:
        print('Please enter your token from Discord below. '
              'You will not need to do this every time you '
              'run Jaffa; this is just first time setup. '
              'You can exit the setup by typing \'exit\'.')
        token = user_input()

        if token.lower() == 'exit':
            os.system('exit')
        else:
            try:
                settings['DISCORD_TOKEN'] = str(token)
                with open('settings.json', 'w') as fp:
                    json.dump(settings, fp, indent=4)
            except:
                print('An error occurred. Aborting setup...')
                os.system('exit')
            else:
                print('Your token has been successfully set. Installing requirements...')
                try:
                    subprocess.call('pip install -r requirements.txt')
                except:
                    print('An error occurred. Aborting setup...')
                    os.system('exit')
                else:
                    print('Requirements successfully installed. Running Jaffa...')
                    subprocess.call('python main.py')
    else:
        print('Please choose an option below using the corresponding number:')
        print('1. Run Jaffa')
        print('2. Pull code from master branch')
        print('3. Pull code from development branch')
        print('4. Update requirements')
        print('5. Quit')
        choice = user_input()
        if choice == '1':
            try:
                subprocess.call('python main.py')
            except:
                print('An error occurred while running Jaffa. Aborting setup...')
                os.system('exit')
        elif choice == '2':
            try:
                subprocess.call('git checkout master')
                subprocess.call('git pull')
            except:
                print('An error occurred while updating Jaffa. Make sure Git is'
                      'installed and available in the PATH environment '
                      'variable. Aborting setup...')
                os.system('exit')
            else:
                print('Jaffa has been successfully updated. Please enter your bot '
                      'token from Discord. Jaffa will then be run automatically.')
                token = user_input()

                try:
                    settings['DISCORD_TOKEN'] = str(token)
                    with open('settings.json', 'w') as fp:
                        json.dump(settings, fp, indent=4)
                except:
                    print('An error occurred. Aborting setup...')
                    os.system('exit')
                else:
                    print('Your token has been successfully set. Running Jaffa...')
                    subprocess.call('python main.py')
        elif choice == '3':
            try:
                subprocess.call('git checkout development')
                subprocess.call('git pull')
            except:
                print('An error occurred while updating Jaffa. Make sure Git is'
                      'installed and available in the PATH environment '
                      'variable. Aborting setup...')
                os.system('exit')
            else:
                print('Jaffa has been successfully updated. Please enter your bot '
                      'token from Discord. Jaffa will then be run automatically.')
                token = user_input()

                try:
                    settings['DISCORD_TOKEN'] = str(token)
                    with open('settings.json', 'w') as fp:
                        json.dump(settings, fp, indent=4)
                except:
                    print('An error occurred. Aborting setup...')
                    os.system('exit')
                else:
                    print('Your token has been successfully set. Running Jaffa...')
                    subprocess.call('python main.py')
        elif choice == '4':
            try:
                subprocess.call('pip install --upgrade -r requirements.txt')
            except:
                print('An error occured while updating Jaffa\'s requirements.'
                      'Aborting setup...')
                os.system('exit')
            else:
                print('Requirements successfully updated. Running Jaffa...')
                subprocess.call('python main.py')
        elif choice == '5':
            os.system('exit')

if __name__ == '__main__':
    main()
