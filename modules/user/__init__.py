<<<<<<< HEAD
from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/user')

from . import views
=======
from flask import Blueprint

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')

from . import views
>>>>>>> cabf5b5b97a2e82ff01e5d1c4308a631f5d67453
