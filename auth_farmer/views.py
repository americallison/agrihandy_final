# This script contains view functions (routes) for the auth_farmer blueprint

from flask import render_template, request, url_for, \
    redirect, flash, session
from datetime import datetime
from agri_app import bcrypt, db
from . import auth_farmer
from .forms import FarmerLoginForm, FarmerSignUpForm
from models import Farmer


@auth_farmer.route('/index', methods=["POST", "GET"])
def index():
    return render_template('auth_farmer/index.html')


# the form is validated and submitted successfully.
@auth_farmer.route('/register', methods=['POST', 'GET'])
def register():
    form = FarmerSignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        farmer = Farmer(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        business_name=form.business_name.data,
                        business_addr=form.business_addr.data,
                        business_contact=form.business_contact.data,
                        website=form.website.data,
                        business_desc=form.business_desc.data,
                        password=password_hash)

        db.session.add(farmer)
        db.session.commit()

        return redirect(url_for('auth_farmer.login'))
    return render_template('auth_farmer/farmer_register.html',
                           current_time=datetime.utcnow(), form=form)


# Create route and view function from login page using auth blueprint
@auth_farmer.route('/login', methods=["POST", "GET"])
def login():
    form = FarmerLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        farmer = Farmer.query.filter_by(email=form.email.data).first()
        if farmer and bcrypt.check_password_hash(farmer.password, form.password.data):
            session['farmer_id'] = farmer.id
            #login_user(farmer, remember=form.remember_me.data)
            #if not farmer.verified:
               # flash("Your business has not been verified by AgriHandy. Verification takes three (3) \
                                     #working days. You will receive an email after verification.")
               # return redirect(url_for('auth_farmer.verify_business'))
            #else:
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else \
                redirect(url_for('auth_farmer.index'))
        else:
            flash("Wrong email or password", "danger")
    return render_template('auth_farmer/farmer_login.html',
                           current_time=datetime.utcnow(), form=form)


@auth_farmer.route('/logout')
def logout():
    if 'farmer_id' in session:
        session.pop('farmer_id', None)
    return redirect(url_for('auth_farmer.login'))


@auth_farmer.route('/verify_business')
def verify_business():
    return render_template('auth_farmer/affirmation.html')

