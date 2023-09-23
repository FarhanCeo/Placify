from flask import Blueprint, render_template, request, redirect, session
from flask_pymongo import MongoClient

student_bp = Blueprint('student', __name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['PMS_100']
print(db)

@student_bp.route('/student_info', methods=['GET', 'POST'])
def student_info():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        email = request.form['email']
        
        # Here you can add code to process and store student information
        # info = {'first_name':first_name,'last_name':last_name,'age':age}

        # st_db_info = db.student_info.find()
        roll_number = session['roll_number']
        # existing_user = db.users.find_one({"roll_number": roll_number})
        # if existing_user:
        #     # User exists, update the information
        #     db.users.update_one({"roll_number": roll_number}, {"$set": {"first_name":first_name ,"last_name": last_name,"age":age,"email":email}})
        #     print("User information updated.")
        
        # User already exists, update the information
        db.users.update_one({"roll_number": roll_number}, {"$set": {"first_name":first_name ,"last_name": last_name,"age":age,"email":email}})
        print("User information updated.")
        user_data = db.users.find_one({"roll_number": roll_number})
        return render_template('Student_profile.html', notification = "User information updated.", user = user_data )
        # else:
        #     # User does not exist, store the new user information
        #     new_user = {'first_name':first_name,'last_name':last_name,'age':age}
        #     db.users.insert_one(new_user)
        #     print("User information stored.")


        # if info not in st_db_info:
        #     db.student_info.insert_one(info)
        # else:
        #     db.student_info.update_one(info)

        # s = db.users.find_one({'roll_number':roll_number})
        # return render_template('student_info.html', info_s = s)

    roll_number = session['roll_number']
    user_data = db.users.find_one({"roll_number": roll_number})
    return render_template('student_form.html', user = user_data)
