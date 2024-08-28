from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


    # as we're working with session, we have to set a secret key
    app.secret_key = "alibaba"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    # define how the login manager loads the user
    # So, when you load a user, you get their uid
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    bcrypt = Bcrypt(app)

    from routes import register_routes
    register_routes(app, db, bcrypt)

    #import models.py later on
    migrate = Migrate(app, db)
    
    return app
