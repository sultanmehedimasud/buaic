import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
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


from modules.user.views import user_bp

app.register_blueprint(user_bp)


from modules.landing.views import landing_bp

app.register_blueprint(landing_bp)

from modules.intake.views import intake_bp

app.register_blueprint(intake_bp)


@app.route('/home')
def home():
    return render_template('landing/index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
