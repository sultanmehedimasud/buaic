from flask import Blueprint, flash

user_bp = Blueprint('user', __name__, url_prefix='/user')

from . import views
from .models import User, db
