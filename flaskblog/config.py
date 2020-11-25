


class Config():
    SECRET_KEY='7bd55caed8226ea2bc04b1ad9fde9073'
    #Specifying path of database
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db' #/// means from current directory create db file
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'YOUR EMAIL'
    MAIL_PASSWORD = 'YOUR PASSWORD'