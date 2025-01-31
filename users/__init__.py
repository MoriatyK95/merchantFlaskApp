# This file sets up the 'users' blueprint, grouping user-related routes together.
from flask import Blueprint

users_bp = Blueprint('users', __name__)

from . import routes