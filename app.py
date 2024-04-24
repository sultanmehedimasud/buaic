import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, abort, flash, render_template
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager.login_view = 'login'

app.secret_key = 'a7q!1rg#(-7n9)tuprhy7k(0pie!0l4$@9j+o_s(wfvcm&qbwq'

app.config['MAIL_DEBUG'] = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

from modules.user.models import User
from modules.user.views import user_bp

app.register_blueprint(user_bp)

from modules.landing.views import landing_bp

app.register_blueprint(landing_bp)

from modules.intake.models import Semester
from modules.intake.views import intake_bp

app.register_blueprint(intake_bp)

from modules.members.views import members_bp

app.register_blueprint(members_bp)

from modules.polls.models import Polls, Voted
from modules.polls.views import polls_bp

app.register_blueprint(polls_bp)

from modules.event.models import Event
from modules.event.views import event_bp

app.register_blueprint(event_bp)

from modules.attendance.models import Attendance
from modules.attendance.views import attendance_bp

app.register_blueprint(attendance_bp)

from modules.resources.models import Booking, Room
from modules.resources.views import resource_bp

app.register_blueprint(resource_bp)

from modules.dashboard.views import dashboard_bp

app.register_blueprint(dashboard_bp)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('landing/index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(403)
def forbidden_error(error):
    code_msg = "403 - Forbidden"
    msg = "You do not have permission to access this page."
    return render_template('error.html', code_msg=code_msg, msg=msg), 403


@app.errorhandler(404)
def not_found_error(error):
    code_msg = "404 - Not Found"
    msg = "The page you are looking for does not exist."
    return render_template('error.html', code_msg=code_msg, msg=msg), 404


@app.errorhandler(500)
def internal_error(error):
    code_msg = "500 - Internal Server Error"
    msg = "Something went wrong on our end. Please try again later."
    return render_template('error.html', code_msg=code_msg, msg=msg), 500

@app.errorhandler(401)
def unauthorized_error(error):
    code_msg = "401 - Unauthorized"
    msg = "You are not authorized to access this page."
    return render_template('error.html', code_msg=code_msg, msg=msg), 401


if __name__ == '__main__':
    app.run(debug=True)
