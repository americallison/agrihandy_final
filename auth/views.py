from agri_app import bcrypt
from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .forms import RegistrationForm, LoginForm, EditAccountForm
from models import User, CartItem
from agri_app import db



def no_of_cart_items():
    if current_user.is_authenticated:
        no_of_items_in_cart = CartItem.query.filter_by(buyer=current_user).count()
    else:
        no_of_items_in_cart = 0
    return no_of_items_in_cart


# This route registers a new customer and adds them to the database.
# The form first checks whether the request method is POST and
# the form is validated and submitted successfully.
@auth.route('/register', methods=['POST', 'GET'])
def register():
    no_of_items_in_cart = no_of_cart_items()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, \
                    last_name=form.last_name.data,
                    email=form.email.data, user_name=form.user_name.data,
                    password=password_hash)
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        #token = user.generate_confirmation_token()
        #send_email(user.email, 'Confirm Your Account',
                   #'auth/email/confirm', user=user, token=token)
        flash('Account successfully created', 'success')
        #flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', current_time=datetime.utcnow(),
                           no_of_items_in_cart=no_of_items_in_cart, form=form)


""""@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Explore AgriHandy.')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))"""


@auth.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_profile():
    no_of_items_in_cart = no_of_cart_items()
    form = EditAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.user_name = form.user_name.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your account details have been updated.', 'success')
        return redirect(url_for('main.account'))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.email.data = current_user.email
    form.user_name.data = current_user.user_name
    return render_template('auth/edit_account.html',
                           no_of_items_in_cart=no_of_items_in_cart,
                           form=form)


# Create route and view function from login page using auth blueprint
@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        session['username'] = form.user_name.data
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page and next_page.startswith('/') \
                else redirect(url_for('main.index'))
        else:
            flash ("Incorrect username or password", "danger")
    return render_template('auth/login.html', current_time=datetime.utcnow(),
                          form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash ('You have been logged out', 'success')
    return redirect(url_for('main.index'))
