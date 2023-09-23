from flask import Blueprint, render_template,request, redirect, url_for
from flask_pymongo import MongoClient

admin_bp = Blueprint('admin', __name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['PMS_100']
print(db)

@admin_bp.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        company = {'name': name, 'description': description}
        db.companies.insert_one(company)
        # companies.append({'name': name, 'description': description})
        return redirect(url_for('company.company_list'))
    return render_template('add_company.html')

@admin_bp.route('/student_list')
def student_list():
    # Here you can retrieve and display the list of registered students
    students = db.users.find()  # Retrieve student data from your database
    return render_template('student_list.html', students=students)
