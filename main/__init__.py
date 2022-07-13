# The main package constructor __init__.py is used to construct the main blueprint.
from flask import Blueprint

# Instantiate the Blueprint object
main = Blueprint('main', __name__)

# Import views.py and errors.py for the main Blueprint to use
from . import views, errors, forms
