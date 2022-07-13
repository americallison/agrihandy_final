# agrihandy.py script creates the flask application and runs it
from agri_app import db, create_agri_app


# Create Flask app with create_agri_app function
# Use settings from DevelopmentConfiguration
app = create_agri_app('default')


if __name__ == "__main__":
    # Make application (app) available for execution
    with app.app_context():
        db.create_all()  # create all database tables (models)
    app.run(port=1000, debug=True)
    # app.run(host='192.168.88.14', port=1000, debug=True)
