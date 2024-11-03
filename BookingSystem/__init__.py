import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from datetime import timedelta
from flask_migrate import Migrate
#from BookingSystem.Admin_Page import admin UserMixin, login_required, login_user, logout_user,   current_user

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2770d4fd598f5a792ebce414a891f412'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5433/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    #app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    #app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
    #app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
    app.config['MAIL_USERNAME'] = 'kf515335@gmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = 'rsjptgkiwfqrxtwx'  # Replace with your email password
    app.config['MAIL_DEFAULT_SENDER'] = 'kf515335@gmail.com'  # Replace with your email
    app.config['SESSION_PERMANENT'] = False 
    app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the filesystem
    app.config['SESSION_PERMANENT'] = True  # Allow sessions to persist
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SESSION_PROTECTION'] = 'strong'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit to 16 MB



    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'main.traveler_login'  # Change 'main.traveler_login' to your login route
    login_manager.login_message_category = 'info'  # Flash message category for unauthorized users
    

    
        # Import and register the blueprint
    from BookingSystem.routes import main  # Ensure you import your blueprint
    from BookingSystem.Admin_Page import admin
    from BookingSystem.TourOperator_Page import touroperator
    from BookingSystem.TourGuide_Page import tourguide
   
  

    
         # Register the blueprint with your app
        
        # Register the admin blueprint from BookingSystem.Admin_Page import adminwith a URL prefix
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin') #####################
    app.register_blueprint(touroperator, url_prefix='/touroperator')
    app.register_blueprint(tourguide, url_prefix='/tourguide')
    


        
    with app.app_context():
        db.create_all()  # Create database tables

    return app




































