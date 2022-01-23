import json
import requests

import colorama
from colorama import Fore


colorama.init(autoreset=True)

id = ''


def menu():
    print(f'\nUser ID: {Fore.LIGHTCYAN_EX}None\n') if id == '' else print(f'User ID: {Fore.LIGHTCYAN_EX}{id}\n')

    print('[1] - Generate user ID')
    print('[2] - Propose a new trip')
    print('[3] - See all proposals')
    print('[4] - Declare interest in a trip')
    print('[5] - Check who\'s interested in your trips')
    print('[6] - Exit system\n')


def generate_id():
    global id
    if id == '':
        response = requests.get('http://localhost:8080/api/v1/id/')
        if response.status_code == 200:
            response_json = json.loads(response.content)
            id = response_json['id']
            print()
        else:
            print(f'\n{Fore.LIGHTRED_EX}[ERROR] Could not perform HTTP request!\n')
    else:
        print(f'\n{Fore.LIGHTYELLOW_EX}[INFO] You can only generate one ID per session!\n')


def main():
    print(Fore.LIGHTGREEN_EX + 'Welcome to the travel service client!')

    while True:
        menu()
        try:
            user_input = input('> ')
        except (KeyboardInterrupt, EOFError):
            print(f'\n{Fore.LIGHTRED_EX}[ERROR] Uh oh... Something unexpected happened. Bye!\n')
            break

        if user_input == '1':
            generate_id()
        elif user_input == '6':
            print(f'\n{Fore.LIGHTMAGENTA_EX}Bye!\n')
            break


if __name__ == '__main__':
    main()
