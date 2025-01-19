# This file is used to create a blueprint for the users module
from flask import Blueprint

users_bp = Blueprint('users', __name__)

from . import routes