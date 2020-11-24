from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', #'Username' is the label
                           validators=[DataRequired(), Length(min=2, max=20) ])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password',
                             validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')
    
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user :
            raise ValidationError("Username Taken. Try different Username")
            
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user :
            raise ValidationError("Email Taken. Try different email")
    
    
    
class LoginForm(FlaskForm):
    

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password',
                             validators=[DataRequired()])
    
    # Let user to stay login using a secure cookie
    
    remember = BooleanField('Remember Me')
    
    
    submit = SubmitField('Login')
    
    
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', #'Username' is the label
                           validators=[DataRequired(), Length(min=2, max=20) ])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','jpeg','png'])])
    
    
    submit = SubmitField('Update')
    
    
    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username = username.data).first()
            if user :
                raise ValidationError("Username Taken. Try different Username")
            
    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email = email.data).first()
            if user :
                raise ValidationError("Email Taken. Try different email")
                

    
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset Password')
    # To check whether email entered is valid or not
    def validate_email(self, email):      
        user = User.query.filter_by(email = email.data).first()
        if user is None :
            raise ValidationError("Email doesnt exist. Please Register")
            
            
            
class ResetPasswordForm(FlaskForm):  
    
    password = PasswordField('Password',
                             validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')