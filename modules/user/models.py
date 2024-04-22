from datetime import datetime

from flask_bcrypt import Bcrypt, generate_password_hash
from flask_login import UserMixin

from app import db

bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.Integer, nullable=False, unique=True)
    rfid = db.Column(db.String(10), nullable=True, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(14), nullable=False, unique=True)
    semester = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    blood_group = db.Column(db.String(3), nullable=False)
    department = db.Column(db.String(35), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    designation = db.Column(db.String(20), default='General Member')
    joined_semester = db.Column(db.String(30), nullable=False)
    tfa = db.Column(db.Boolean, default=False, nullable=False)
    otp = db.Column(db.String(6), nullable=True)
    reset_token = db.Column(db.String(100), unique=True)
    
    def set_password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password, password)
    
    def get_id(self):
        return str(self.id)
