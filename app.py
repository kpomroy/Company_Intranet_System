from flask import Flask, render_template, request, redirect, url_for, g
import traceback
from password import authenticate, hash_pw, password_strength, generate_password
from database import add_user, get_access_level, get_password, get_all_usernames

app = Flask(__name__)

loginAttempts = 1

# Function to validate user credentials
def login(username, password):
    usernames = get_all_usernames()
    print(usernames)
    if username in usernames:
        storedPassword = get_password(username)
        return authenticate(storedPassword, password)
    return False

# Function to verify if an employee has access to the menu option they chose
# admin: full access
# accountant: access to Time Reporting, Accounting, IT Helpdesk, and Exit
# engineer: access to Time Reporting, IT Helpdesk, Engineering Documents, and Exit
# intern: access to Time Reporting, IT Helpdesk, and Exit
def checkEmployeeAccess(username, choice):
    accessLevel = get_access_level(username)
    if(accessLevel == 'admin'):
        return True
    elif(accessLevel == 'accountant'):
        if (choice != 4):
            return True
        else:
            return False
    elif(accessLevel == 'engineer'):
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

# Flask route for new user page
@app.route('/new_user', methods= ['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # check if username is available
        if username not in get_all_usernames():
            # validate password
            if password_strength(password):
                hashedPassword = hash_pw(password)
                add_user(username, hashedPassword)
                return redirect('/')
            else:
                return render_template('new_user.html', error = 'Password not complex enough')
        else:
            return render_template('new_user.html', error='Username not available')
    return render_template('new_user.html')

# Flask route for new user page with generated password
@app.route('/new_user/password', methods= ['GET', 'POST'])
def create_user_password():
    randPassword = generate_password()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # check if username is available
        if username not in get_all_usernames():
            # validate password
            if password_strength(password):
                hashedPassword = hash_pw(password)
                add_user(username, hashedPassword)
                return redirect('/')
            else:
                return render_template('new_user.html', error = 'Password not complex enough')
        else:
            return render_template('new_user.html', error='Username not available')
    return render_template('new_user.html', password=randPassword)

# Flask route for the menu page
@app.route('/menu/<username>')
def menu(username):
    return render_template('menu.html', username=username)


# Flask route for handling menu options
@app.route('/menu_option/<username>/<int:choice>')
def menu_option(username, choice):
    if checkEmployeeAccess(username, choice):
        if choice == 1:
            return f'You accessed the Time Reporting area'
        elif choice == 2:
            return f'You accessed the Accounting area'
        elif choice == 3:
            return f'You accessed the IT Helpdesk area'
        elif choice == 4:
            return f'You accessed the Engineering Documents area!'
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
        app.run(debug=True, host='localhost', port=8097)
    except Exception as err:
        traceback.print_exc()