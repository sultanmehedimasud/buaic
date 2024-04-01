from flask import Blueprint

event_bp = Blueprint('event', __name__, template_folder='templates', static_folder='static')

from . import views 