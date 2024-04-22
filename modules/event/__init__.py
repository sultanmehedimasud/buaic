from flask import Blueprint, flash

event_bp = Blueprint('event', __name__, template_folder='templates', static_folder='static', url_prefix='/event')

from . import views
