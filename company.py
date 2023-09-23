from flask import Blueprint, render_template
from flask_pymongo import MongoClient

company_bp = Blueprint('company', __name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['PMS_100']
print(db)
companies = db.companies.find()

# companies = [
#     {'name': 'Company A', 'description': 'A software development company'},
#     {'name': 'Company B', 'description': 'An e-commerce platform'},
#     {'name': 'Company C', 'description': 'A renewable energy company'}
# ]

@company_bp.route('/company_list')
def company_list():
    return render_template('company_list.html',companies = companies)
