from flask import Blueprint, flash

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

from . import views
