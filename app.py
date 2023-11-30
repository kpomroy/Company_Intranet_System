from flask import Flask, render_template, request, redirect, url_for, g
import traceback
import csv
from password_crack import authenticate

app = Flask(__name__)

loginAttempts = 1


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

# Flask route for the login page
@app.route('/', methods=['GET', 'POST'])
def login_page():
    global loginAttempts
    if request.method == 'POST' and loginAttempts < 3:
        username = request.form['username']
        password = request.form['password']
        if login(username, password):
            # Reset attempts on successful login
            loginAttempts = 0
            return redirect(url_for('menu', username=username))
        else:
            loginAttempts += 1
            return render_template('login.html', error='Invalid username or password')
    elif loginAttempts == 3:
        return 'You are locked from the system for too many attempts'
    else:
        return render_template('login.html', error=None)

# Flask route for the menu page
@app.route('/menu/<username>')
def menu(username):
    return render_template('menu.html', username=username)


# Flask route for handling menu options
@app.route('/menu_option/<username>/<int:choice>')
def menu_option(username, choice):
    if checkEmployeeAccess(username, choice):
        if choice == 1:
            return f'You accessed the Time Reporting area, {username}!'
        elif choice == 2:
            return f'You accessed the Accounting area, {username}!'
        elif choice == 3:
            return f'You accessed the IT Helpdesk area, {username}!'
        elif choice == 4:
            return f'You accessed the Engineering Documents area, {username}!'
        else:
            return 'Exiting the system'
    else:
        return 'You are not authorized to access this area'

# Flask route for the exit option
@app.route('/exit')
def exit():
    return 'Exiting the system'

# Flask route for a new user
@app.route('/new_user')
def new_user():
    return render_template('new_user.html')

if __name__ == '__main__':
    try:
        getEmployeeInfo()
        app.run(debug=True, host='localhost', port=8097)
    except Exception as err:
        traceback.print_exc()