# This script contains view functions (routes) for the main application.

from flask import render_template, session, redirect, url_for, \
    request, flash
from flask_login import current_user, login_required
from models import *
import os
import secrets
from agri_app.email import send_email
from sqlalchemy import desc
import uuid
from werkzeug.utils import secure_filename
from . import main
from .forms import ProductForm, OrderForm, CartForm, PaymentForm, \
    ForgotPasswordForm, EditProductForm, CategoryForm

# create variables (UPLOAD FOLDER) to hold uploads of pictures
UPLOAD_FOLDER = 'agri_app/static/products_imgs/'

# create variable (ALLOWED_EXTENSIONS) to specify uploads type
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}


# Create routes using the main (blueprint) prefix
@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0

    category = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount,
         Products.date_posted, Products.location).filter_by(
        category_name='Vegetables').order_by(desc(
        Products.date_posted)).limit(4)

    category_1 = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount).filter_by(
        category_name='Fruits').order_by(desc(Products.date_posted)).limit(4)

    category_2 = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount).filter_by(
        category_name='Tuber Crop').order_by(
        desc(Products.date_posted)).limit(4)

    category_3 = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount).filter_by(
        category_name='Poultry').order_by(desc(
        Products.date_posted)).limit(4)

    category_4 = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount).filter_by(
        category_name='Fishery').order_by(desc(Products.date_posted)).limit(4)

    category_5 = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount).filter_by(
        category_name='Livestock/Ruminants').order_by(desc(Products.date_posted)).limit(4)

    return render_template('index.html',
                           category=category,
                           category_1=category_1, category_2=category_2,
                           category_3=category_3, category_4=category_4,
                           category_5=category_5,
                           cart_length=cart_length,
                           title="Home"
                           )


@main.route('/contact')
def contact():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    return render_template('contact-us.html', cart_length=cart_length)


@main.route('/ussd')
def ussd():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    return render_template('ussd.html', cart_length=cart_length)


# Show all the products posted by farmers
@main.route('/show_products')
def show_products():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    page = request.args.get('page', 1, type=int)
    product = Products.query.order_by(
        desc(Products.date_posted)).paginate(page=page, per_page=12)
    return render_template('products.html',
                           current_time=datetime.datetime.utcnow(),
                           product=product, title="All Products",
                           cart_length=cart_length)


# Show details of products posted by farmers
@main.route('/product_details/<int:product_id>')
# @login_required
def product_details(product_id):
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    form = CartForm()
    product = Products.query.filter_by(id=product_id).first_or_404()
    return render_template('product_details.html',
                           current_time=datetime.datetime.utcnow(),
                           product=product,
                           form=form, cart_length=cart_length,
                           title="Product Details")


# Show product form for farmers to post product
# Only users registered as farmers can post products
@main.route('/add_product', methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    category_form = CategoryForm()
    try:
        if not 'farmer_id' in session:
            flash('Please login as a farmer to add product.')
            return redirect(url_for('auth_farmer.login'))
        if form.validate_on_submit():
            product_img = request.files['product_picture']
            filename = str(uuid.uuid1()) + os.path.splitext(
                secure_filename(product_img.filename))[1]
            product_img.save(os.path.join(UPLOAD_FOLDER, filename))
            product = Products(product_name=form.product_name.data,
                               unit_price=form.unit_price.data,
                               unit_of_measure=form.unit_of_measure.data,
                               available_quan=form.quantity_available.data,
                               discount=form.discount.data,
                               location=form.location.data,
                               product_img=filename,
                               product_description=
                               form.product_description.data,
                               contact_num=form.contact_num.data,
                               farmer_id=session['farmer_id']
                               )
            db.session.add(product)
            db.session.commit()
            category = Category(
                category_name=category_form.category_name.data,
                product_id=product.id)
            db.session.add(category)
            db.session.commit()
            flash('Product added successfully', 'success')
            return redirect(url_for('auth_farmer.index'))
    except Exception as e:
        flash("Error posting product. Please login as a farmer or \
              try again.")
        return redirect(url_for('auth_farmer.login'))
    return render_template('auth_farmer/add_products.html',
                           current_time=datetime.datetime.utcnow(),
                           form=form, category_form=category_form,
                           title="Add Product"
                           )

'''
# Route to allow farmers to edit products from their end
@main.route('/edit_cart/<int:product_id>', methods=['GET', 'POST'])
def edit_cart(product_id):
    cart1 = CartItem.query.filter_by(productid=product_id).first()
    form = EditCartForm()
    if form.validate_on_submit():
        cart1.quantity = form.quantity.data
        product_to_add = CartItem(productid=product_id,
                                  quantity=form.quantity.data,
                                  user_id=current_user.id)
        db.session.add(product_to_add)
        flash('Your purchase quantity has been updated.', 'success')
        return redirect(url_for('main.my_cart'))
    form.quantity.data = cart1.quantity
    return render_template('edit_cart.html',
                           form=form,
                           cart1=cart1)'''


# Route to allow farmers to edit products from their end
@main.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    try:
        farmer_id = session['farmer_id']
        if 'farmer_id' not in session:
            flash('Please login as a farmer to add product.')
            return redirect(url_for('auth_farmer.login'))
        product = Products.query.filter_by(id=product_id).first()
        form = EditProductForm()
        if form.validate_on_submit():
            product.product_name = form.product_name.data
            product.product_description = form.product_description.data
            product.unit_price = form.unit_price.data
            product.available_quan = form.quantity_available.data
            product.unit_of_measure = form.unit_of_measure.data
            product.discount = form.discount.data
            product.location = form.location.data
            product.contact_num = form.contact_num.data
            db.session.commit()
            flash('Your product details have been updated.', 'success')
            return redirect(url_for('main.my_products_list',
                                    farmer_id=farmer_id))
        form.product_name.data = product.product_name
        form.product_description.data = product.product_description
        form.unit_price.data = product.unit_price
        form.quantity_available.data = product.available_quan
        form.unit_of_measure.data = product.unit_of_measure
        form.discount.data = product.discount
        form.location.data = product.location
        form.contact_num.data = product.contact_num
    except Exception as e:
        flash("Error editing product. Please login as a farmer or try again.")
        return redirect(url_for('auth_farmer.login'))
    return render_template('auth_farmer/edit_products.html',
                           form=form,
                           product=product)


# Shows products only for farmers that posted them
@main.route('/my_products')
def my_products_list():
    global my_product
    global my_category

    # page = request.args.get('page', 1, type=int)
    try:
        # create session variable 'farmer_id' to use in query
        farmer_id = session['farmer_id']
        prod = Products.query.filter_by(farmer_id=farmer_id).count()
        my_product = Products.query.filter_by(
            farmer_id=farmer_id).all()
        my_category = Category.query.all()
        if 'farmer_id' in session:
            return render_template('my_products.html',
                                   my_product=my_product,
                                   my_category=my_category, prod=prod,
                                   title="My Products")
    except Exception as e:
        flash('Error viewing products. Please log in as a farmer.')
        return redirect(url_for('auth_farmer.login'))
    return render_template('auth_farmer/index.html',
                           title="Farmer's Home")


# Route to allow farmers to delete products they posted
@main.route('/remove_from_list/<int:product_id>')
def remove_from_list(product_id):
    product_to_remove = Products.query.filter_by \
        (id=product_id).first_or_404()
    db.session.delete(product_to_remove)
    db.session.commit()
    flash('You removed an item from your list of products!', 'success')
    return redirect(url_for('main.my_products_list',
                            farmer_id=session["farmer_id"]))


# Route to show customer cart
@main.route('/my_cart', methods=["GET", "POST"])
@login_required
def my_cart():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    cart = Products.query.join(CartItem). \
        add_columns(CartItem.quantity, Products.id, Products.unit_price,
                    Products.product_name,
                    Products.id, Products.product_img, Products.discount,
                    Products.unit_of_measure).filter_by(
        buyer=current_user).all()

    cart1 = CartItem.query.filter_by(productid=Products.id, buyer=current_user).first()
    total_cost = 0
    discount_ = 0
    pre_cost = 0

    for item in cart:
        pre_cost += float(item.unit_price * item.quantity)
        discount_ += ((item.unit_price * item.discount / 100) * item.quantity)
        session['pre_total'] = str(pre_cost)
        session['discounted'] = str(discount_)

    for product in cart:
        total_cost += float((product.unit_price - product.unit_price *
                             product.discount / 100)) * float(
            product.quantity)
        session['total_price'] = total_cost

    return render_template('cart_.html', cart=cart, cart_length=cart_length,
                           total_cost=total_cost,
                           discount_=discount_, pre_cost=pre_cost,
                           cart1=cart1, title="My Bag")


# Route to allow customers add products to their cart
@main.route('/add_to_cart/<product_id>', methods=["GET", "POST"])
@login_required
def add_to_cart(product_id):
    form = CartForm()
    cart_row = CartItem.query.filter_by(productid=product_id,
                                        buyer=current_user).first()
    if cart_row:
        cart_row.quantity += form.quantity.data
        db.session.commit()
        flash('Product is in bag. ' + " " + str(form.quantity.data)
              + " " + 'more added.', 'success')
    else:
        product_to_add = CartItem(productid=product_id,
                                  quantity=form.quantity.data,
                                  user_id=current_user.id)
        db.session.add(product_to_add)
        db.session.commit()
        flash('Product has been added to cart.', 'success')
    return redirect(url_for('main.show_products'))


# Route to allow customers delete products from their cart
@main.route('/remove_product/<int:product_id>')
@login_required
def remove_product(product_id):
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    product_to_remove = CartItem.query.filter_by(
        productid=product_id, buyer=current_user).first()
    db.session.delete(product_to_remove)
    db.session.commit()
    # reduce cart length by one if user deletes product from cart
    cart_length -= 1
    flash('You removed an item from your cart!', 'success')
    return redirect(url_for('main.my_cart'))


# Show order form for buyers to order farm products
# Only users registered as buyers can order products


@main.route('/make_order', methods=['GET', 'POST'])
@login_required
def make_order():
    global order_items

    order_items = {}

    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(
            buyer=current_user).count()
    else:
        cart_length = 0

    cart = Products.query.join(CartItem).add_columns(
        CartItem.quantity, Products.id, Products.unit_price,
        Products.product_name,
        Products.product_img, Products.discount,
        Products.unit_of_measure).filter_by(
        buyer=current_user).all()

    form = OrderForm()
    if form.validate_on_submit():

        order = Order(order_number=secrets.token_hex(6),
                      total_price=session.get('total_price'), customer_name=
                      form.full_name.data, delivery_address=form.delivery_address.data,
                      contact=form.contact.data, comments=form.comments.data)

        db.session.add(order)
        db.session.flush()

        for item in cart:
            order_items['order_item'] = item
            order_item = OrderItem(order_id=order.id, product=item.id,
                                   price=item.unit_price, quantity=item.quantity,
                                   total=int(item.unit_price) * int(item.quantity))
            db.session.add(order_item)
            db.session.commit()

        db.session.commit()

        session['order'] = order.id

        order_items = list(order_items)

        return redirect(url_for('main.make_payment'))
    return render_template("add_orders.html",
                           current_time=datetime.datetime.utcnow(),
                           form=form,
                           cart_length=cart_length, cart=cart,
                           total_cost=session.get('total_price'),
                           order_items=order_items)


# Shows options for farmers to view/products they posted
@main.route('/farmer_dashboard/int:<farmer_id>')
@login_required
def farmer_dashboard(farmer_id):
    prod = Products.query.filter_by(farmer_id=farmer_id).count()
    return render_template('farmer_dashboard.html',
                           prod=prod)


# Show account details of a logged in user
@main.route('/account')
def account():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    return render_template('account.html', current_time=datetime.datetime.utcnow(),
                           cart_length=cart_length)


@main.route('/forgot_password')
def forgot_password():
    form = ForgotPasswordForm()
    return render_template('forgot_password.html', form=form)


""""# Show all buyer orders.
# Only buyers can access this page
@main.route('/my_orders/<user_id>')
@roles_required('Buyer')
def my_orders(user_id):
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    order = Order.query.filter_by(user_id=user_id, buyer=current_user).all()
    order_item = OrderItem.query.filter_by(order_id=Order.id).first()
    return render_template('my_orders.html', current_time=datetime.datetime.utcnow(),
                           order=order, order_item=order_item, Title='My Orders',
                           cart_length=cart_length)"""


# Show available payment platforms
@main.route('/make_payment', methods=["GET", "POST"])
@login_required
def make_payment():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    form = PaymentForm()

    if form.validate_on_submit():
        payment = Payment(orange_mon_num=form.orange_mon_num.data,
                          currency=form.currency.data,
                          receiver_orange_mon_num=form.producer_number.data,
                          amount=form.amount.data,
                          user_id=current_user.id,
                          order_id=session.get('order'))
        db.session.add(payment)

        if form.amount.data != session.get('total_price'):
            flash('Please check the amount!!', 'info')
            return redirect(url_for('main.make_payment'))

        db.session.commit()

        order = Order.query.filter_by(id=session.get('order')).first_or_404()
        order.paid = True
        db.session.add(order)

        # delete items from cart after user makes payment
        cart_to_delete = CartItem.query.filter_by(
            user_id=current_user.id).all()
        for item in cart_to_delete:
            if cart_to_delete is not None:
                db.session.delete(item)
                db.session.commit()

        return redirect(url_for('main.transaction_details'))
    return render_template('payment_page.html',
                           current_time=datetime.datetime.utcnow(),
                           cart_length=cart_length, form=form,
                           order_cost=session.get('total_price'))


@main.route('/transaction_details')
@login_required
def transaction_details():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    payment = Payment.query.join(Order).add_columns \
        (Order.order_number, Order.total_price,
         Order.order_item, Order.customer_name,
         Order.delivery_address, Order.contact,
         Payment.receiver_orange_mon_num,
         Payment.amount, Payment.currency,
         Payment.orange_mon_num).filter_by(
        id=session['order']
    ).first()
    return render_template('transaction_details.html', payment=payment,
                           cart_length=cart_length)


@main.route('/vegetables_all')
def vegetables():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    page = request.args.get('page', 1, type=int)
    category = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount,
         Products.date_posted).order_by(desc(Products.date_posted)).filter_by(
        category_name='Vegetables').paginate(page=page, per_page=12)
    return render_template('vegetables_all.html', category=category,
                           cart_length=cart_length)


@main.route('/fruits_all')
def fruits():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    page = request.args.get('page', 1, type=int)
    category = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount,
         Products.date_posted).order_by(desc(Products.date_posted)).filter_by(
        category_name='Fruits').paginate(page=page, per_page=12)
    return render_template('fruits_all.html', category=category,
                           cart_length=cart_length, title="Vegetables")


@main.route('/tuber_crops')
def tuber_crops():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    page = request.args.get('page', 1, type=int)
    category = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount,
         Products.date_posted).order_by(desc(Products.date_posted)).filter_by(
        category_name='Tuber Crop').paginate(page=page, per_page=12)
    return render_template('tuber_crops.html', category=category,
                           cart_length=cart_length, title="Tuber Crops")


@main.route('/poultry')
def poultry():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    page = request.args.get('page', 1, type=int)
    category = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount,
         Products.date_posted).order_by(desc(Products.date_posted)).filter_by(
        category_name='Poultry').paginate(page=page, per_page=12)
    return render_template('poultry.html', category=category,
                           cart_length=cart_length)


@main.route('/fishery_all')
def fishery_all():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    page = request.args.get('page', 1, type=int)
    category = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount,
         Products.date_posted).order_by(desc(Products.date_posted)).filter_by(
        category_name='Fishery').paginate(page=page, per_page=12)
    return render_template('fishery_all.html', category=category,
                           cart_length=cart_length, title="Fishery")


@main.route('/livestock_ruminant')
def livestock_ruminant():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    page = request.args.get('page', 1, type=int)
    category = Products.query.join(Category).add_columns \
        (Category.category_name, Products.unit_price, Products.product_name,
         Products.product_img, Products.id, Products.discount,
         Products.date_posted).order_by(desc(Products.date_posted)).filter_by(
        category_name='Livestock/Ruminants').paginate(page=page, per_page=12)
    return render_template('livestock_ruminant.html', category=category,
                           cart_length=cart_length)


@main.route('/search')
def product_search():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('query')
    product = Products.query.msearch(keyword, fields=['product_name']). \
        order_by(desc(Products.date_posted)).paginate(page=page, per_page=12)
    return render_template('search.html', title='Searching for' + keyword,
                           product=product, cart_length=cart_length)


# Will be added soon
'''@main.route('/weather_info')
def weather_info():
    '''


@main.route('/sell_agrihandy')
def sell_agrihandy():
    return render_template('sell_agrihandy.html')


@main.route('/about')
def about():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    return render_template('about.html', cart_length=cart_length)


@main.route('/terms_con')
def terms_con():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    return render_template('terms_con.html', cart_length=cart_length)


@main.route('/blog')
def blog():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    return render_template('blog.html', cart_length=cart_length)


'''
@main.route('/send_news')
def send_news():
    form = NewsletterForm()
    send_email(form.email_address.data, 'Thanks for subscribing',
    'auth/email/newsletter')
    return redirect(url_for('index'))'''


@main.route('/market_prices')
def market_prices():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    return render_template('market_prices.html', cart_length=cart_length)


@main.route('/faq')
def faq():
    if current_user.is_authenticated:
        cart_length = CartItem.query.filter_by(buyer=current_user).count()
    else:
        cart_length = 0
    return render_template('faq.html', cart_length=cart_length)
