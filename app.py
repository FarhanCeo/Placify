from flask import Flask
from index import *
from student import *
from company import *
from authentication import *
from admin import *

# Create a Flask web application instance
app = Flask(__name__)

app.register_blueprint(bp)
app.register_blueprint(student_bp,url_prefix='/student')
app.register_blueprint(company_bp,url_prefix='/companies')
app.register_blueprint(authh)
app.register_blueprint(admin_bp, url_prefix='/admin')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
