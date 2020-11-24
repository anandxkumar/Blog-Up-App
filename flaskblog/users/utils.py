import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail, app




def save_picture(form_picture): # input will be form.picture.data, directory of the image

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    # file name that needs to be saved
    picture_fn = random_hex + f_ext 
    picture_path = os.path.join(app.root_path,"static/profile_pic/"+picture_fn)
    output_size =(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


def send_reset_email(user):
    token =  user.get_reset_token()
    msg= Message('Password Reset Request', 
                 sender = 'noreply@ok.com',
                 recipients = [user.email])
    
    msg.body = f''' To reset your password click the below link :
{url_for('users.reset_token',token = token, _external = True)}

If request not sent by u simply ignore'''

    mail.send(msg)