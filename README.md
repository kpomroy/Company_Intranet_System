## Kevin Pomroy
## CS 2660
## Principles of Cybersecurity
## Final Project
## Secure Company Login Site

# Overview
This flask app models a company intranet system which requires a valid employee username and password to login. Access to certain features within the website is dependent on the users access level (admin, accountant, engineer, intern). User information is stored in an SQLite database and new users can create accounts. Passwords are hashed and stored in the database. 

# Running and testing
To set up the database, either include the user.db file in the directory, or uncomment the bottom section of the database.py file and run the program. To start the flask app, run app.py and follow the link to the site. 

For testing, the usernames and passwords are as follows:
kevin, Password123!
eric, Password123!
rye, Password123!
harry, Password123!