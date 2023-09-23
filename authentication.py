from flask import Blueprint, render_template,request,session
from flask_pymongo import MongoClient
import bcrypt
from flask_session import Session

authh = Blueprint('auth', __name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['PMS_100']
print(db)


# Sample user data for demonstration purposes
# users = {
#     "user1": "password1",
#     "user2": "password2",
#     "admin": "admin"
# }

# Define a route for the login page
@authh.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        password = request.form['password']

        admin = db.admin.find_one({'roll_number': roll_number})
        if roll_number == 'admin' and admin['password'] == password:
            return render_template('admin.html')

        # if username in users and users[username] == password:
        #     return render_template('Student_profile.html', username = username)
        # else:
        #     return "Invalid username or password. Please try again."

        user = db.users.find_one({'roll_number': roll_number})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['roll_number'] = roll_number
            session['email'] = user['email']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            user_data = db.users.find_one({"roll_number": roll_number})
            return render_template('Student_profile.html', user = user_data)
        else:
            return "Invalid username or password. Please try again."

    return render_template('login.html')


@authh.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove 'username' from the session to log out the user
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('roll_number', None)
    session.pop('email', None)
    return render_template('index.html')


@authh.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        roll_number = request.form['roll_number']
        password = request.form['password']
        email = request.form['email']

        existing_user = db.users.find_one({"roll_number": roll_number})
        if existing_user:
            # User exists, update the information
            db.users.update_one({"roll_number": roll_number}, {"$set": {"first_name": first_name,"last_name": last_name}})
            print("User information updated.")
        else:
            # User does not exist, store the new user information
            # Here you would typically add code to store the user's information in a database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_data = {'first_name': first_name, 'last_name': last_name, "roll_number": roll_number,'password': hashed_password, 'email': email}
            db.users.insert_one(user_data)
            # new_user = {'first_name':first_name,'last_name':last_name,'age':age}
            # db.users.insert_one(new_user)
            print("User information stored.")
        return render_template('login.html')
    return render_template('registration.html')