# Initializing everything

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_mail import Mail
from flaskblog.config import Config


# WILL PROTECT US FROM FORGARY ATTACK AND MODIFYING CACHE
'''import secrets
   secrets.token_hex(16)'''
   

# Database
db = SQLAlchemy()

bcrypt =  Bcrypt()

login_manager = LoginManager()

login_manager.login_view = 'users.login' #login is function name of route
login_manager.login_message_category = 'info' #Bootstrap library to imporve looks

mail = Mail()




def create_app(config_class = Config):
    app = Flask(__name__) # module name __name__
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    
   # IT WILL BE EXECUTED FROM RUN.PY TO LOAD OTHER MODULES AND TO AVOID CIRCULAR LOOP
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app
 