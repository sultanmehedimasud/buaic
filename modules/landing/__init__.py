from flask import Blueprint, flash

landing_bp = Blueprint('landing', __name__)

from . import views
