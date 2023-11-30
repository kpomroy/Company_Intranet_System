# Final Project
# Kevin Pomroy
# CS 2660 / Fall 2023
#
# This program creates a login interface and menu 
# to a company intranet system that requires 
# users (employees) to enter a username and password
# in order to view a menu of options.


# Use a dictionary to store employees usernames and passwords
import csv
from password_crack import authenticate

# Dictionaries for employee credentials and access levels
employeeLogins = {}
employeeAccess = {}
employeeDataFile = 'data/employeeData.csv'

# Function to retrieve employee login info and access info from the csv and save it in two dicitonaries
def getEmployeeInfo():
    try:
        with open(employeeDataFile, 'r') as file:
            csvreader = csv.reader(file)
            # skip header row
            next(csvreader, None)

            for row in csvreader:
                username, hashedPassword, access_level = row
                # populate dictionaries
                employeeLogins[username] = hashedPassword
                employeeAccess[username] = access_level
    except FileNotFoundError:
        print(f"File '{employeeDataFile}' not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to validate user credentials
def login(username, password):
    if username in employeeLogins:
        storedPassword = employeeLogins[username]
        return authenticate(storedPassword, password)
    return False

# Function to display the menu options
def displayMenu():
    print('')
    print('Company Intranet System Menu')
    print('1. Time Reporting')
    print('2. Accounting')
    print('3. IT Helpdesk')
    print('4. Engineering Documents')
    print('5. Exit')
    print('')

# Function to get and validate user input on which menu option they select
def getMenuChoice():
    choice = input("Choose a menu option: ")
    while(choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5'):
        print("Invalid choice")
        choice = input("Choose a menu option: ")
    return int(choice)
    
# Function to give the user the option to return to the menu or exit the system
def returnToMenuOption():
    print("")
    menuOrExit = input('Press 0 to return to the menu or 5 to exit the system: ')
    while(menuOrExit != '0' and menuOrExit != '5'):
        print('')
        print('Invalid input')
        print('')
        menuOrExit = input('Press 0 to return to the menu or 5 to exit the system: ')
    if(menuOrExit == '0'):
        return True
    else:
        print('Exiting the system')
        exit()

# Function to verify if an employee has access to the menu option they chose
# admin: full access
# accountant: access to Time Reporting, Accounting, IT Helpdesk, and Exit
# engineer: access to Time Reporting, IT Helpdesk, Engineering Documents, and Exit
# intern: access to Time Reporting, IT Helpdesk, and Exit
def checkEmployeeAccess(username, choice):
    if(employeeAccess[username] == 'admin'):
        return True
    elif(employeeAccess[username] == 'accountant'):
        if (choice != 4):
            return True
        else:
            return False
    elif(employeeAccess[username] == 'engineer'):
        if (choice != 2):
            return True
        else:
            return False
    else:
        if (choice != 2 and choice != 4):
            return True
        else:
            return False

def main():
    # fill dictionaries with info from csv
    getEmployeeInfo()

    print('Welcome to the Company Intranet System')
    print('Please log in to access the menu')

    # loop until valid login credentials are given
    valid = False
    while(not valid):
        username = input('Username: ')
        password = input('Password: ')

        # try to login using given username and password
        if(login(username,password)):
            print('Access granted')
            valid = True
        else:
            print('Invalid username or password or both')
            print('Please try again')
    
    # continue program until user wants to exit
    while(True):
        # display the menu and get user choice
        displayMenu()
        choice = getMenuChoice()

        # valideate that employee has access to their menu choice
        if(checkEmployeeAccess(username, choice)):
            if(choice == 1):
                print('You accessed the Time Reporting area')
            elif(choice == 2):
                print('You accessed the Accounting area')
            elif(choice == 3):
                print('You accessed the IT Helpdesk area')
            elif(choice == 4):
                print('You accessed the Engineering Documents area')
            else:
                print('Exiting the system')
                exit()
        else:
            print('You are not authorized to access this area')

        # allow users to either return to the menu to make another choice or exit
        returnToMenuOption()

main()
