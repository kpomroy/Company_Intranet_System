"""
SQLite Python Database
"""

import sqlite3
from datetime import datetime


def create_db():
    """ Create table 'users' in 'user' database """
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users
                    (
                    username text,
                    hashedPassword text,
                    accessLevel text
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def get_date():
    """ Generate timestamp for data inserts """
    d = datetime.now()
    return d.strftime("%m/%d/%Y, %H:%M:%S")


def add_user(username, hashedPassword, role = ''):
    if role == '':
        role = 'intern'
    data_to_insert = [(username, hashedPassword, role)]
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.executemany("INSERT INTO users VALUES (?, ?, ?)", data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Record added")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def clear_table():
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("DELETE FROM users")
        conn.commit()
    except sqlite3.OperationalError:
        print("Error. Could not clear table.")
    else:
        print("Table cleared")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def get_password(username):
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        for row in c.execute("SELECT hashedPassword FROM users WHERE username='" + username + "'"):
            password = row[0]
        return password
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def query_db():
    """ Display all records in the table """
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM users"):
            print(row)
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


# add_user('kevin', 'f26d84aa5a093ea43137e50dcc3ba6747d7815d3aa9319f3f6894600f5599728cd45cb069cb2262c5d37e79fc7f7ba10314d65af49146cd97b99b0b2', 'admin')
# add_user('eric', '3abad61c46327e9c269e5a37f25b3afb7f7e50c946d719fd7a9dc803a62d19300cae5fa6301da887feb0980b7c0a25721291d62afd9ac7e3858a0a27', 'accountant')
# add_user('rye', '80cb2ae3e5effc043ba0964f600a5dd6176204e2decd7077cb4fca8682bb18399078ff0fcbbd9486701e887c8df6d4d5ec6ff9a9fe9646fa56fcf259', 'engineer')
# add_user('harry', '357ab90b53c995deebf1e5ca8b508b471f262d6b51f053db3b6f9db8c119e130ac52415451a141d1f252ad932d89eb2f8c7145adf51c0f5b2722a770', 'intern')
query_db()

#print(get_password('kevin'))

