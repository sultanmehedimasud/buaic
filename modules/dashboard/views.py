from datetime import datetime

from flask import Blueprint, render_template
from flask_login import login_required

from app import db
from modules.event.models import Event
from modules.user.views import User

from . import dashboard_bp


@dashboard_bp.route('/')
@login_required
def dashboard():
    now = datetime.now()

    next_event = Event.query.filter(Event.start_date > now).order_by(Event.start_date.asc()).first()

    if next_event:
        return render_template('dashboard/dashboard.html', next_event=next_event)
    else:
        return render_template('dashboard/dashboard.html', next_event=None)