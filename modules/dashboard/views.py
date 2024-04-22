from datetime import datetime

from flask import Blueprint, abort, flash, render_template
from flask_login import login_required

from app import db
from modules.event.models import Event

from . import dashboard_bp


@dashboard_bp.route('/')
@login_required
def dashboard():
    now = datetime.now()
    next_event = Event.query.filter(Event.start_date > now).order_by(Event.start_date).first()
        
    return render_template('dashboard/dashboard.html', next_event=next_event)
