from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
DB_NAME = "database.db"
socketio = SocketIO()  

# factory function to create the Flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'seophonebookabcd123livelaughlove'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
   
    # initialize the database and socketio
    db.init_app(app)
    socketio.init_app(app)  
  
    # Import the Blueprints#
    from .views import views
    from .auth import auth
    from .profile import profile
    from .tags import tags
    from .interests import interests
    from .models import User

    # Register the Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/')
    app.register_blueprint(tags, url_prefix='/')
    app.register_blueprint(interests, url_prefix='/')

    # Create the database if it does not exist
    create_database(app)

    # Set up the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Load the user for the login manager
    @login_manager.user_loader
    def load_user(id):
       return User.query.get(int(id))

    return app

# Function to create the database if it does not exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
       with app.app_context():
        db.create_all()
        print('Created Database!')
        
        
