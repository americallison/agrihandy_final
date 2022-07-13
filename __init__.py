# import Flask and its extensions and other modules
from flask import Flask
from flask_bootstraps import Bootstrap4
from flask_bcrypt import Bcrypt
from config import config
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData
from admin_ import AgrihandyAdmin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_msearch import Search
import uuid


# change SQLAlchemy naming conventions of constraints
def auto_constraint_name(constraint):
    if constraint.name is None or constraint.name == '_unnamed_':
        return "sa_autoname_%s" % str(uuid.uuid4())[0:5]
    else:
        return constraint.name


convention = {
    'auto_constraint_name': auto_constraint_name,
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
    }

metadata = MetaData(naming_convention=convention)

# Create uninitialized flask extensions
'''At this point, there is no application instance (app) to initialize
   the extensions with. 
'''
bootstrap = Bootstrap4()
mail = Mail()
moment = Moment()
db = SQLAlchemy(metadata=metadata)
login_manager = LoginManager()
admin1 = Admin(name='AgriHandy Admin')
from models import User, Products, CartItem, Farmer,\
    FarmerVerify, Order, OrderItem, Category, Payment
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to have full access"
login_manager.login_message_category = "info"
csrf = CSRFProtect()
migrate = Migrate()
bcrypt = Bcrypt()
search = Search(db=db)


# The create_app function contains the application instance and name
# of configuration imported from config.py

def create_agri_app(config_name): # factory function
    app = Flask(__name__)  # create Flask application instance (app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)  # initialize the type of configuration
    # Complete initialization of flask extensions
    bootstrap.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    admin1.init_app(app, index_view=AgrihandyAdmin(User, db.session,
                                                   url='/admin', endpoint='admin'))
    admin1.add_view(AgrihandyAdmin(Products, db.session))
    admin1.add_view(ModelView(CartItem, db.session))
    admin1.add_view(AgrihandyAdmin(OrderItem, db.session))
    admin1.add_view(AgrihandyAdmin(Order, db.session))
    admin1.add_view(AgrihandyAdmin(Payment, db.session))
    admin1.add_view(AgrihandyAdmin(Category, db.session))
    admin1.add_view(AgrihandyAdmin(Farmer, db.session))
    admin1.add_view(AgrihandyAdmin(FarmerVerify, db.session))
    search.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    # Register main blueprint within the app package constructor for usability
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register auth blueprint within the app package constructor for usability
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Register auth_farmer blueprint within the app package constructor for usability
    from .auth_farmer import auth_farmer as auth_farmer_blueprint
    app.register_blueprint(auth_farmer_blueprint, url_prefix='/auth_farmer')

    return app
