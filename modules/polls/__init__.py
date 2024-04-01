#bluprint
from flask import Blueprint

polls_bp = Blueprint('polls', __name__, template_folder='templates', static_folder='static')

from . import views