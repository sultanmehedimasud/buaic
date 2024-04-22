from flask import Blueprint, flash

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

from . import views
