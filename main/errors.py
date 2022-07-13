from flask import render_template
from datetime import datetime
from . import main


# View function for 404 error (page not found)
@main.app_errorhandler(404)
def page_not_found(err):
    return render_template('errors/404.html', title='404 - Page Not Found'), 404


# View function for 500 error (internal server error)
@main.app_errorhandler(500)
def internal_server_error(err):
    return render_template('errors/500.html', title='500 - Internal Server Error'), 500
