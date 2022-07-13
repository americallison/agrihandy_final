# This script contains code for forms used in the main application
# Classes are written for forms based on the function of the form


# import FlaskForm class from flask_wtf
from flask_wtf import FlaskForm
# import fields used in forms from wtforms
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, DecimalField, IntegerField
# import various validators from wtforms.validators
from wtforms.validators import InputRequired, DataRequired, Length, Optional, Email, NumberRange, Regexp
from flask_wtf.file import FileAllowed, FileField, FileRequired


# The ProductForm class inherits from FlaskForm
class ProductForm(FlaskForm):
    """The ProductForm class inherits from the base class FlaskForm. All
           methods of FlaskForm are available for use in the ProductForm
           class
        """
    product_name = StringField('Product Name',
                               validators=[InputRequired
                                           (message='Product Name Required'),
                                           Length(min=1, max=100)])
    product_description = TextAreaField(
        'Description', validators=[InputRequired
                                           (message='Description Required'),
                                           Length(min=1, max=300)])
    unit_of_measure = SelectField('Product Unit', validators=[InputRequired()],
                                  choices=[("None", "(Select Unit of Measure)"),
                                           ("bag", "(bag)"), ("kilo", "(kg)"),
                                           ("jar", "(jar)"),
                                           ("bucket", "(bucket)"),
                                           ("cartoon", "(cartoon)"),
                                           ("chick", "(chick)"),
                                           ("rooster", "(rooster)"),
                                           ("hen", "(hen)")])
    unit_price = DecimalField("Price per Unit", validators=[InputRequired()])
    discount = IntegerField("Discount", validators=[Optional(),
                                                    NumberRange(min=1)])
    quantity_available = IntegerField('Available Quantity',
                                      validators=[InputRequired(),
                                                  NumberRange(
                                                      min=5)])
    location = StringField("Product Location", validators=[
        InputRequired(message="Location Required")])
    product_picture = FileField("Product Photo", validators=[
        FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'giff', 'pdf', 'docx'])])
    contact_num = StringField("Contact Number", validators=[
        InputRequired(), Length(min=10, max=13)])
    post_product = SubmitField("Post Product")


class EditProductForm(FlaskForm):
    product_name = StringField(validators=[Length(min=0, max=100)])
    product_description = TextAreaField(validators=[Length(min=0,max=500)])
    unit_price = DecimalField('Unit Price')
    unit_of_measure = SelectField('Product Unit', validators=[Optional()],
                                  choices=[("None", "(Select Unit of Measure)"),
                                      ("bag", "(bag)"), ("kilo", "(kg)"),
                                           ("jar", "(jar)"),
                                           ("bucket", "(bucket)"),
                                           ("cartoon", "(cartoon)"),
                                           ("chick", "(chick)"),
                                           ("rooster", "(rooster)"),
                                           ("hen", "(hen)")])
    discount = IntegerField('Discount', validators=[Optional()])
    quantity_available = IntegerField(validators=[Optional(),
                                                  NumberRange(
                                                      min=5)
                                                  ])
    location = StringField(validators=[Length(min=0, max=100)])
    contact_num = StringField('Phone number', validators=[Length(min=0, max=15)])
    update_product = SubmitField('Update Product')


class CategoryForm(FlaskForm):
    category_name = SelectField('Product Category', validators=[Optional()],
                                   choices=[('None', 'Select category'),
                                            ('Vegetables', 'Vegetables'),
                                            ('Fruits', 'Fruits'),
                                            ('Tuber Crop', 'Tuber Crop'),
                                            ('Poultry', 'Poultry'),
                                            ('Fishery', 'Fishery'),
                                            ('Livestock/Ruminants', 'Livestock/Ruminants')])


class PaymentForm(FlaskForm):
    orange_mon_num = StringField("Orange Money Number", validators=[
        InputRequired(), Length(min=10,max=10),
        Regexp(regex='[0-9]',message="Please enter your orange number, \
                                            (eg. 0775178202)")])
    currency = SelectField('Currency', validators=[InputRequired()],
                            choices=[('None', 'Select Currency'),
                                        ('LRD', 'Liberian Dollars'),
                                        ('USD','United States Dollars')
                                        ])
    producer_number = StringField("Receiver Number", validators=
    [DataRequired(), Length(min=10, max=13), Regexp(regex='[0-9]')])
    amount = DecimalField("Amount", validators=[InputRequired(),
                          NumberRange(min=1, max=100000000000)])
    pin = PasswordField("Orange Money Pin", validators=
    [InputRequired(), Length(min=4,max=4),Regexp(regex='[0-9]',
                                                message="Pin should be 4 digits (eg. 1994)")])

    submit_payment = SubmitField("Make Payment")


class NewsletterForm(FlaskForm):
    email_address = StringField('Email Address', validators=[InputRequired(),
                                                             Email()])
    send_message = SubmitField("Subscribe")


class OrderForm(FlaskForm):
    full_name = StringField("Full Name", validators=[InputRequired()])
    delivery_address = TextAreaField("Delivery Address", validators=[
        InputRequired()])
    contact = IntegerField("Customer Contact", validators=[InputRequired()
                           ])
    comments = TextAreaField("Additional Comments", validators=[Optional()])
    submit_order = SubmitField("Proceed to Payment")


class CartForm(FlaskForm):
    quantity = IntegerField('Purchase Quantity', validators=[InputRequired(),
                                                             NumberRange(min=1,max=1000)])
    submit_info = SubmitField('Add to Cart')


class EditCartForm(FlaskForm):
    quantity = IntegerField('Purchase Quantity', validators=[Optional(),
                                                             NumberRange(min=1,max=1000)])
    update_cart = SubmitField('Update Cart')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Enter Email', validators=[InputRequired(), Email()])
    submit_email = SubmitField('Send')