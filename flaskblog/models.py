from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager,app    # from __init__.py
from flask_login import UserMixin # Includes Is_active,is_authenicated,get_id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): #UserMixin provides default implementations for the methods that Flask-Login expects user objects to have.
    id =  db.Column(db.Integer, primary_key = True) # Defining a column of integer type
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), unique = False, nullable = False)
 
    image_file = db.Column(db.String(20), nullable = False, default = "default.jpg")# loads default image
    posts = db.relationship('Post', backref = 'author', lazy = True) # Relationship with Post class, backref by which we can find author of post
    
    def get_reset_token(self, expires_sec = 1800):
        s =  Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s =  Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    
    def __repr__(self):  # Prints object when used print user
        return f"User('{self.username}','{self.email}','{self.image_file}')"



class Post(db.Model):
    id =  db.Column(db.Integer, primary_key = True) # Defining a column of integer type
    title = db.Column(db.String(100), unique = False, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) # object user has id which is foreign key
    
    def __repr__(self):  # Prints object when used print post
        return f"User('{self.title}','{self.date_posted}')"# -*- coding: utf-8 -*-

