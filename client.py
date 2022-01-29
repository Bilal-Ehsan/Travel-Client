from email import message
import json
import requests

import colorama
from colorama import Fore


colorama.init(autoreset=True)

user_id = ''
proposals = []


def menu():
    print(f'\nUser ID: {Fore.LIGHTCYAN_EX}None\n') if user_id == '' else print(f'User ID: {Fore.LIGHTCYAN_EX}{user_id}\n')

    print('[1] - Generate user ID')
    print('[2] - Propose a new trip')
    print('[3] - See all proposals')
    print('[4] - Declare interest in a trip')
    print('[5] - Check who\'s interested in your trips')
    print('[6] - Exit system\n')


def generate_user_id():
    global user_id
    if user_id == '':
        response = requests.get('http://localhost:8080/api/v1/id/')
        if response.ok:
            response_json = json.loads(response.content)
            user_id = response_json['id']
            print()
        else:
            print(f'\n{Fore.LIGHTRED_EX}[HTTP ERROR] Could not generate user ID!')
    else:
        print(f'\n{Fore.LIGHTYELLOW_EX}[INFO] You can only generate one user ID per session!\n')


def generate_message_id():
    response = requests.get('http://localhost:8080/api/v1/id/')
    if response.ok:
        response_json = json.loads(response.content)
        return response_json['id']
    else:
        print(f'\n{Fore.LIGHTRED_EX}[HTTP ERROR] Could not generate message ID!')


def propose_trip():
    if user_id != '':
        location = input('\nWhat is the location of the trip? ')
        date = input('What is the date of the trip (YYYY-MM-DD)? ')

        message_id = generate_message_id()
        if message_id == None: return
        
        payload = {
            'user_id': user_id,
            'message_id': message_id,
            'trip_location': location.lower(),
            'trip_date': date
        }

        response = requests.post('http://localhost:8080/api/v1/propose-trip/', data=payload)
        if response.ok:
            print(f'\n{Fore.LIGHTGREEN_EX}[SUCCESS] You successfully proposed a trip!\n')
        else:
            print(f'\n{Fore.LIGHTRED_EX}[HTTP ERROR] Could not perform propose trip!\n')
    else:
        print(f'\n{Fore.LIGHTYELLOW_EX}[INFO] You need a user ID in order to submit a proposal!')


def display_proposals():
    print(f'\n{Fore.LIGHTMAGENTA_EX}Trips:\n')
    for proposal in proposals:
        print(proposal)


def retrieve_proposals():
    response = requests.get('http://localhost:8080/api/v1/trip/')
    if response.ok:
        response_json = json.loads(response.content)
        for i in response_json:
            proposal_data = i.split('&')
            proposal = []
            for i in proposal_data:
                proposal_values = i.split('=')
                proposal.append(proposal_values)

            proposal_dict = {
                'user_id': proposal[0][1],
                'message_id': proposal[1][1],
                'trip_location': proposal[2][1],
                'trip_date': proposal[3][1]
            }

            location = proposal_dict.get('trip_location')
            date = proposal_dict.get('trip_date')

            # Get corresponding weather data for each proposal
            response = requests.get(f'http://localhost:8080/api/v1/forecast?location={location}&date={date}')
            if response.ok:
                weather_data = json.loads(response.content)
                proposal_dict['description'] = weather_data['description']
                proposal_dict['temp'] = weather_data['temp']
            else:
                print(f'\n{Fore.LIGHTRED_EX}[HTTP ERROR] Could not get weather data!')

            proposal_json = json.dumps(proposal_dict)
            proposals.append(proposal_json)
            display_proposals()

    else:
        print(f'\n{Fore.LIGHTRED_EX}[HTTP ERROR] Could not generate message ID!')


def main():
    print(Fore.LIGHTGREEN_EX + 'Welcome to the travel service client!')

    while True:
        menu()
        try:
            user_input = input('> ')
        except (KeyboardInterrupt, EOFError):
            print(f'\n\n{Fore.LIGHTRED_EX}[ERROR] Uh oh... Something unexpected happened. Bye!\n')
            break

        if user_input == '1':
            generate_user_id()
        elif user_input == '2':
            propose_trip()
        elif user_input == '3':
            retrieve_proposals()
        elif user_input == '6':
            print(f'\n{Fore.LIGHTMAGENTA_EX}Bye!\n')
            break


if __name__ == '__main__':
    main()
