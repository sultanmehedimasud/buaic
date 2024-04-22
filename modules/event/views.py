from datetime import datetime
from xml.dom import ValidationErr

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, current_user, login_manager,
                         login_required, login_user, logout_user)

from app import db, login_manager
from modules.attendance.models import Attendance
from modules.intake.models import Semester
from modules.user.models import User

from . import event_bp
from .models import Event

bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title'].upper()
        description = request.form['description']
        start_date = request.form['start_datetime']
        end_date = request.form['end_datetime']
        venue = request.form['venue']
        
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        if start_date < datetime.now():
            flash('Start date cannot be before today', 'danger')
            return redirect(url_for('event.create'))

        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        if end_date < start_date:
            flash('End date cannot be before start date', 'danger')
            return redirect(url_for('event.create'))

        event = Event(title=title, description=description, start_date=start_date, end_date=end_date, venue=venue)
        db.session.add(event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('event.list'))

    return render_template('events/create.html')


@event_bp.route('/list')
@login_required
def list():
    events = Event.query.order_by(Event.start_date.desc()).all()
    now = datetime.now()
    
    return render_template('events/list.html', events=events, now=now)


@event_bp.route('/delete/<int:event_id>', methods=['GET', 'POST'])
@login_required
def delete(event_id):
    if request.method == 'POST':
        event = Event.query.get(event_id)
        attendances = Attendance.query.filter_by(event_id=event_id).all()
        
        for attendance in attendances:
            db.session.delete(attendance)
        
        db.session.delete(event)
        db.session.commit()

        flash('Event deleted successfully!', 'success')
        return redirect(url_for('event.list'))
    

def validate_start_date(start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
    if start_date < datetime.now():
        flash('Start date can not be before today')
        return redirect(url_for('event.create'))

