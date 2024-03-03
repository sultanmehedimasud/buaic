from flask import Blueprint

intake_bp = Blueprint('intake', __name__, url_prefix='/intake')

from . import models, views
