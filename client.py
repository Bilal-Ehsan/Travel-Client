import colorama
from colorama import Fore


colorama.init(autoreset=True)

id = None


def menu():
    print(f'User ID: {id}\n')
    print('[1] - Generate user ID')
    print('[2] - Propose a new trip')
    print('[3] - See all proposals')
    print('[4] - Declare interest in a trip')
    print('[5] - Check who\'s interested in your trips')
    print('[6] - Exit system\n')


def main():
    print(Fore.LIGHTGREEN_EX + 'Welcome to the travel service client!\n')

    while True:
        menu()
        try:
            user_input = input('> ')
        except (KeyboardInterrupt, EOFError):
            print(Fore.LIGHTRED_EX + 'Uh oh... Something unexpected happened. Bye!\n')
            break

        if user_input == '1':
            # TODO: Generate a user ID, which is displayed in the menu
            pass
        elif user_input == '6':
            print(Fore.LIGHTMAGENTA_EX + 'Bye!\n')
            break


if __name__ == '__main__':
    main()
