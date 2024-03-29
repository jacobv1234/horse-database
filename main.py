import csv
import os
horses = []
with open('horses.csv') as horse_csv:
    reader = csv.reader(horse_csv)
    for row in reader:
        horses.append(row)

# horses[0] is the column names
        

print('\u2658\u265e HORSE DATABASE VIEWER \u265e\u2658')
def menu():
    print('''---------------------------
Select one:
1) View all of the information about a horse given its name
2) As 1, but by microchip number
3) Add/edit a horse's additional information
4) Get all horses in a given location
5) Change the location of a horse
6) Change a horse's dental due date
7) Move a horse to removed_horses.csv
8) Exit
---------------------------
Enter the number of your choice below''')
    while True:
        choice = input('>>> ')
        try:
            if int(choice) >= 1 and int(choice) <= 8:
                return int(choice)
            else:
                print('Number must be within the valid range')
        except ValueError:
            print('Please enter a number')


def presence_checked_input(prompt: str = '>>> '):
    while True:
        answer = input(prompt)
        if answer != '':
            return answer
        else:
            print('Please enter a value')

def save_horse(horse):
    horse_copy = horse[:]
    for i in range(len(horse_copy)):
        if horse_copy[i] == '':
            horse_copy[i] = 'UNKNOWN'
    with open(f'{horse_copy[1]}.txt', 'w') as save:
        save.write(f'''Information about {horse_copy[1]}:

Date of arrival:  {horse_copy[0]}
Colour:  {horse_copy[2]}
Sex:  {horse_copy[3]}
Year of Birth:  {horse_copy[4]}

Has a passport:  {horse_copy[5]}
Passport Number:  {horse_copy[6]}
Microchip Number:  {horse_copy[7]}

Location: {horse_copy[8]}
Dental Due Date: {horse_copy[9]}

Additional information:
{horse_copy[10]}''')


def search_for_name(name: str):
    for horse in horses[1:]:
        if horse[1] == name:
            return horse
    return -1

def search_for_chip(chip: str):
    for horse in horses[1:]:
        if chip in horse[7]:
            return horse
    return -1


def save_csv():
    with open('horses.csv','w') as horse_csv:
        writer = csv.writer(horse_csv, lineterminator='\n')
        writer.writerows(horses)
    content = ''
    with open('horses.csv','r') as f:
        content = f.read()
    content.replace('\n\n', '\n')
    while True:
        if content[-1] == '\n':
            content = content[:-1]
        else:
            break
    with open('horses.csv', 'w') as f:
        f.write(content)


def save_removed():
    with open('removed_horses.csv','w') as horse_csv:
        writer = csv.writer(horse_csv, lineterminator='\n')
        writer.writerows(removed_horses)
    content = ''
    with open('removed_horses.csv','r') as f:
        content = f.read()
    content.replace('\n\n', '\n')
    while True:
        if content[-1] == '\n':
            content = content[:-1]
        else:
            break
    with open('removed_horses.csv', 'w') as f:
        f.write(content)


def list_locations():
    locations = []
    for horse in horses:
        if horse[8] not in locations:
            print(horse[8])
            locations.append(horse[8])
    return locations



while True:
    choice = menu()
    print('---------------------------')
    match choice:
        # stop
        case 8:
            exit()
        
        # search by name
        case 1:
            print('Enter the name of the horse')
            name = presence_checked_input().upper()
            print('---------------------------')
            horse = search_for_name(name)
            if horse == -1:
                print(f'Unable to find horse named {name}')
            else:
                save_horse(horse)
                print(f"{name}'s information has been saved to a file called {name}.txt")
        
        # search by microchip
        case 2:
            print('Enter the microchip number:')
            chip = presence_checked_input()
            print('---------------------------')
            horse = search_for_chip(chip)
            if horse == -1:
                print(f'Unable to find horse with this number')
            else:
                save_horse(horse)
                print(chip, 'corresponds to', horse[1])
                print(f"{horse[1]}'s information has been saved to a file called {horse[1]}.txt")
        
        # edit note
        case 3:
            print('Enter the name of the horse')
            name = presence_checked_input().upper()
            print('---------------------------')
            horse = search_for_name(name)
            if horse == -1:
                print(f'Unable to find horse named {name}')
            else:
                with open('additional_info.txt', 'w') as f:
                    f.write(horse[-1])
                print('''A file has been created called additional_info.txt.
Edit this text file to have the new information,
then come back here and press enter.''')
                input()
                with open('additional_info.txt', 'r') as f:
                    horse[-1] = f.read().strip('\n')
                os.remove('additional_info.txt') 
        
        # all horses in a location
        case 4:
            print('Enter the location from the options below:')
            locations = list_locations()
            while True:
                location = presence_checked_input()
                if location not in locations:
                    print('Not one of the options!')
                    continue
                break
            for horse in horses:
                if horse[8] == location:
                    print(f'Name: {horse[1]} Microchip: {horse[7]}')
        

        # change location
        case 5:
            print('Enter the name of a horse to move')
            name = presence_checked_input().upper()
            print('---------------------------')
            horse = search_for_name(name)
            if horse == -1:
                print(f'Unable to find horse named {name}')
            else:
                print(f'This horse is currently at {horse[8]}')
                print('Enter the location from the options below (or type in a new one):')
                locations = list_locations()
                location = presence_checked_input()
                location = location.upper()
                horse[8] = location
        

        # change dental due date
        case 6:
            print('Enter the name of a horse to edit')
            name = presence_checked_input().upper()
            print('---------------------------')
            horse = search_for_name(name)
            if horse == -1:
                print(f'Unable to find horse named {name}')
            else:
                print(f'{horse[1]} has a due date of {horse[9]}')
                print('Enter the new date in the format DD/MM/YY')
                date = presence_checked_input()
                horse[9] = date


        # move horse to removed_horses
        case 7:
            print('Enter the name of a horse to remove')
            name = presence_checked_input().upper()
            print('---------------------------')
            horse = search_for_name(name)
            if horse == -1:
                print(f'Unable to find horse named {name}')
            else:
                print(f'Are you sure {horse[1]} is the right horse? (y/n)')
                decision = presence_checked_input()
                if decision == 'y':
                    removed_horses = []
                    with open('removed_horses.csv') as horse_csv:
                        reader = csv.reader(horse_csv)
                        for row in reader:
                            removed_horses.append(row)
                    removed_horses.append(horse)
                    horses.remove(horse)
                    save_removed()



    save_csv()
    input('Press Enter to continue')