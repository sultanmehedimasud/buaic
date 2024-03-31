from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, current_user, login_manager,
                         login_required, login_user, logout_user)

# from app import db, login_manager
from extensions import db, login_manager
from modules.intake.models import Semester

from .models import User

import re

user_bp = Blueprint('user', __name__, url_prefix='/user')

bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_last_semester():
    last_semester = Semester.query.order_by(Semester.semester_name.desc()).first()

    if last_semester:
        return last_semester.semester_name
    else:
        return 'Default Semester'

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        email = request.form.get('email')
        phone = request.form.get('phone')
        semester = request.form.get('semester')
        dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').date()
        blood_group = request.form.get('blood_group')
        preferred_department = request.form.get('preferred_department')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('user.register'))
        
        #strong password check
        if not is_strong_password(password):
            flash('Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.', 'danger')
            return redirect(url_for('user.register'))
       
        #phone number validation
        if not is_valid_phone(phone):
            flash('Invalid phone number.')
            return redirect(url_for('user.register'))
          
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        last_semester = get_last_semester()

        user = User(
            name=name,
            student_id=student_id,
            email=email,
            phone=phone,
            semester=semester,
            dob=dob,
            blood_group=blood_group,
            department=preferred_department,
            joined_semester=last_semester,
            password=hashed_password,
        )
        
        db.session.add(user)
        db.session.commit()
    
        flash('Registration pending approval.')
        return redirect(url_for('home'))

    return render_template('auth/registration.html')

#function to check if phone number is valid
def is_valid_phone(phone):
    if len(phone) != 11:
        return False
    return True

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('auth/login.html')

@user_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        student_id = request.form.get('student_id')  

        #if all fields are empty
        if not email or not student_id:
            flash('All fields are required.')
            return redirect(url_for('user.forgot_password'))
        user = User.query.filter_by(email=email, student_id=student_id).first()  # Check both email and id
        


        if user:
            session['reset_password_email'] = email
            return redirect(url_for('user.reset_password', email=email))
        else:
            flash('User not found.')


    return render_template('auth/forgot_password.html')

@user_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        # email = request.form.get('email')
        email = session.get('reset_password_email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        #if all fields are empty
        if not email or not new_password or not confirm_password:
            flash('All fields are required.')
            return redirect(url_for('user.reset_password', email=email))
        

        # print(email, new_password, confirm_password)

        if new_password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('user.reset_password', email=email))
        
        #strong password check
        if not is_strong_password(new_password):
            flash('Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.', 'danger')
            return redirect(url_for('user.reset_password', email=email))

        user = User.query.filter_by(email=email).first()

        if user:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!')
            return redirect(url_for('user.login'))
        else:
            flash('Invalid email', 'danger')

    return render_template('auth/reset_password.html')

def is_strong_password(password):
    if (len(password) < 8 or
        not re.search("[a-z]", password) or
        not re.search("[A-Z]", password) or
        not re.search("[0-9]", password) or
            not re.search("[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True

#change password
@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        #if fields are empty
        if not current_password or not new_password or not confirm_password:
            flash('All fields are required.')
            return redirect(url_for('user.change_password'))

        if new_password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('user.change_password'))

        #strong password check
        if not is_strong_password(new_password):
            flash('Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.', 'danger')
            return redirect(url_for('user.change_password'))

        user = User.query.get(current_user.id)

        if user and user.check_password(current_password):
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Password changed successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect current password.', 'danger')

    return render_template('auth/change_password.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))
