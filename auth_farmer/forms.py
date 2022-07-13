# import FlaskForm class from flask_wtf
from flask_wtf import FlaskForm
# import fields used in forms from wtforms
from wtforms import StringField, SubmitField, PasswordField, BooleanField, \
    TextAreaField
# import various validators from wtforms.validators
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo, \
    Optional, Email, URL, ValidationError
from models import Farmer


class FarmerSignUpForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[InputRequired(),
                                         Length(min=1, max=100)])
    last_name = StringField('Last Name',
                            validators=[InputRequired(),
                                        Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(),
                                             Length(min=1, max=100)])
    business_name = StringField('Business Name',
                                validators=[
                                    InputRequired(message="Please enter business name"),
                                            Length(min=1, max=150)])
    business_addr = TextAreaField('Business Address',
                                validators=[InputRequired(),
                                            Length(min=1, max=200)])
    business_contact = StringField('Phone Number', validators=[InputRequired(),
                                                        Length(min=10,
                                                               max=20)])
    website = StringField('Business Web URL', validators=[Optional(),
                                                              URL()])
    #business_logo = FileField('Business Logo', validators=[FileAllowed(['jpg','png','giff']),
                                                #           Optional()])
    business_desc = TextAreaField('Business Description', validators=[InputRequired()])


    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=8, max=100)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=
                                     [EqualTo('password',
                                              message='Both passwords should match')])
    terms_conditions = BooleanField("I agree to AgriHandy terms and conditions",
                                    validators=[InputRequired()])
    submit_info = SubmitField('Register as Farmer')


    def validate_business_name(self, business_name):
        farmer_business_name = Farmer.query.filter_by(business_name=business_name.data).first()
        if farmer_business_name:
            raise ValidationError("That business nae has been used to create an \
                                           account. Please choose another business name.")

    def validate_email(self, email):
        farmer_email = Farmer.query.filter_by(email=email.data).first()
        if farmer_email:
            raise ValidationError("That email has been used to create an \
                                           account. Please use another email.")


class FarmerLoginForm(FlaskForm):
    """The SupplierLoginForm class inherits from the base class FlaskForm.
    """
    email = StringField('Email', validators=[InputRequired(), Email(),
                                                   Length(min=1, max=100)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=1, max=100)])
    remember_me = BooleanField('Remember Me', validators=[Optional()])
    submit_info = SubmitField('Login as Farmer')


class FarmerVerifyForm(FlaskForm):
    """The FarmerVerifyForm class inherits from the base class FlaskForm.
    """
    email = StringField('Email', validators=[InputRequired(), Email(),
                                                   Length(min=1, max=100)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=1, max=100)])
    remember_me = BooleanField('Remember Me', validators=[Optional()])
    submit_info = SubmitField('Login as Farmer')