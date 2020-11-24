from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)



@users.route("/register", methods = ['GET','POST']) #route defines webpage "/resgister" means about registration 
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    # To check the values entered is correct of not
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data} ! You can now login", "success")
        return redirect(url_for('users.login'))
    return render_template('register.html', title = "Register", form=form)

@users.route("/login", methods = ['GET','POST']) #route defines webpage
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            # next parameter if it exists
            next_page = request.args.get('next')
            if next_page:
                return redirect(url_for('users.account'))
            flash("Successfully Logged In !", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Please check your email and password", "danger") #!danger =  for red alert
            
    return render_template('login.html', title = "Login", form=form)

@users.route("/logout", methods = ['GET','POST'])
def logout():
    logout_user() #logging out 
    return redirect(url_for('main.home'))


@users.route("/account", methods = ['GET','POST'])
@login_required # Used to check that login is required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account has been updated","success")
        return redirect(url_for('users.account'))
    elif request.method == 'GET': # If we load the webpage
        form.email.data = current_user.email
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pic/'+ current_user.image_file)
    return render_template('account.html', title = "Account", image_file = image_file,form= form)



# When clicking user it will display all the posts posted by this user
@users.route("/user/<string:username>") 
def user_posts(username):
    user = User.query.filter_by(username = username).first_or_404()
    # getting page number request when html file send page number in url_for
    page = request.args.get('page',1,type = int)
    post = Post.query.filter_by(author = user)\
                               .order_by(Post.date_posted.desc())\
                               .paginate(page = page, per_page = 3)
    return render_template('user_post.html',posts = post,title = username ,user = user) # posts variable is passed having value post


@users.route("/reset_request", methods = ['GET','POST'])
def reset_request():  
    # If user is logged in then redirect to home page
    if current_user.is_authenticated:
       return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to your email with instructions for resetting password","info")
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',form=form,title = 'Reset Request') # posts variable is passed having value post


#for resetting password
@users.route("/reset_request/<token>", methods = ['GET','POST'])
def reset_token(token):  
    # If user is logged in then redirect to home page
    if current_user.is_authenticated:
       return redirect(url_for("main.home"))
    # To check whether the token is valid or expired or not
    user= User.verify_reset_token(token) 
    if user is None:
        flash("That is an invalid token or expired token !","warning")
        return redirect(url_for('users.reset_request'))
    

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user.password = hashed_password
        db.session.commit()
        flash("Password successfully Resetted ! ", "success")
        return redirect(url_for('users.login'))
    return render_template('reset_password.html',form=form,title = 'Reset Password') # posts variable is passed having value post
