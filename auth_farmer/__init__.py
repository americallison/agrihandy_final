# The main package constructor __init__.py is used to construct the main blueprint.
from flask import Blueprint

# Instantiate the Blueprint object
auth_farmer = Blueprint('auth_farmer', __name__)

# Import views.py and errors.py for the auth_farmer Blueprint to use
from . import views, forms