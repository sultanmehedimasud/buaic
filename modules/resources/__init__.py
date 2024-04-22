from flask import Blueprint, flash

resource_bp = Blueprint('resources', __name__, template_folder='templates', static_folder='static')

from . import views
