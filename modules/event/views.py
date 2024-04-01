from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, current_user, login_manager,
                         login_required, login_user, logout_user)

# from app import db, login_manager
from extensions import db, login_manager
from modules.intake.models import Semester
from modules.user.models import User
from . models import Event

event_bp = Blueprint('event', __name__, url_prefix='/event')

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
        date = request.form['datetime']
        venue = request.form['venue']

        event = Event(title=title, description=description, date=date, venue=venue)
        db.session.add(event)
        db.session.commit()

        flash('Event created successfully', 'success')
        return redirect(url_for('event.list'))

    return render_template('events/create.html')


@event_bp.route('/list')
@login_required
def list():
    events = Event.query.all()
    total_events = Event.query.count()
    return render_template('events/list.html', events=events, total_events=total_events)

@event_bp.route('/show/<int:event_id>')
@login_required
def show(event_id):
    event = Event.query.get(event_id)
    return render_template('events/show.html', event=event)

#delete event
@event_bp.route('/delete/<int:event_id>')
@login_required
def delete(event_id):
    event = Event.query.get(event_id)
    db.session.delete(event)
    db.session.commit()

    flash('Event deleted successfully', 'success')
    return redirect(url_for('event.list'))

