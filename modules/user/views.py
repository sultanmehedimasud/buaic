from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, current_user, login_manager,
                         login_required, login_user, logout_user)

from app import db, login_manager
from modules.intake.models import Semester

from .models import User

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

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))
