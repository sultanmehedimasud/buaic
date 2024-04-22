from flask import Blueprint, flash

intake_bp = Blueprint('intake', __name__, url_prefix='/intake')

from . import models, views
