# The auth package constructor __init__.py is used to construct the main blueprint.
from flask import Blueprint

# Instantiate the Blueprint object
auth = Blueprint('auth', __name__)

# Import views.py and errors.py for the auth Blueprint to use
from . import views, forms
