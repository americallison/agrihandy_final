# import FlaskForm class from flask_wtf
from flask_wtf import FlaskForm
# import current_user from flask_login
# import fields used in forms from wtforms
from wtforms import StringField, SubmitField, PasswordField, BooleanField
# import various validators from wtforms.validators
from wtforms.validators import InputRequired, Length, EqualTo, \
    Optional, Email, ValidationError, Regexp
from models import User


# Create SignUpForm for registration of regular users
class RegistrationForm(FlaskForm):
    """The RegisterForm class inherits from the base class FlaskForm. All
       methods of FlaskForm are available for use in the RegisterForm
       class
    """
    first_name = StringField('First Name', validators=[InputRequired(),
                                                       Length(min=1, max=100)])
    last_name = StringField('Last Name', validators=[InputRequired(),
                                                     Length(min=1, max=100)])
    email = StringField('Email', validators=[Optional(), Email(),
                                             Length(min=1, max=100)])
    user_name = StringField('Username', validators=[InputRequired(),
                                                    Length(min=1, max=100),
                                                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                    'Usernames should have letters, \
                            numbers, underscores, or dots')])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=8, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo(
        'password', message='Both passwords should match')])
    terms_conditions = BooleanField("I agree to AgriHandy terms and conditions",
                                    validators=[InputRequired()])
    submit_info = SubmitField('Register')

    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError("This username has been used to create an \
                                   account. Please choose another username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email has been used to create an \
                                   account. Please use another email.")


# create Login from for regular user login
class LoginForm(FlaskForm):
    """The LoginForm class inherits from the base class FlaskForm. All
       methods of FlaskForm can now be used in the LoginForm class
    """
    user_name = StringField(validators=[InputRequired(),
                                        Length(min=1, max=15)])
    password = PasswordField(validators=[InputRequired(),
                                         Length(min=1, max=100)])
    remember_me = BooleanField(validators=[Optional()])
    submit_info = SubmitField('Login')


class EditAccountForm(FlaskForm):
    first_name = StringField(validators=[Length(min=0, max=100)])
    last_name = StringField(validators=[Length(min=0, max=100)])
    email = StringField('Email', validators=[Length(min=0, max=100)])
    user_name = StringField(validators=[Length(min=0, max=100)])
    submit_info = SubmitField('Update Account')



