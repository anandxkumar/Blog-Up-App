# Initializing everything
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_mail import Mail

app = Flask(__name__) # module name __name__

# WILL PROTECT US FROM FORGARY ATTACK AND MODIFYING CACHE
'''import secrets
   secrets.token_hex(16)'''
   
app.config['SECRET_KEY']='7bd55caed8226ea2bc04b1ad9fde9073'

#Specifying path of database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db' #/// means from current directory create db file

# Database
db = SQLAlchemy(app)

bcrypt =  Bcrypt()

login_manager = LoginManager(app)
login_manager.login_view = 'users.login' #login is function name of route
login_manager.login_message_category = 'info' #Bootstrap library to imporve looks

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'YOUR EMAIL'
app.config['MAIL_PASSWORD'] = 'YOUR PASSWORD'


mail = Mail(app)


# IT WILL BE EXECUTED FROM RUN.PY TO LOAD OTHER MODULES AND TO AVOID CIRCULAR LOOP
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)