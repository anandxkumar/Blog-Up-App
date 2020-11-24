from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route("/") #route defines webpage
#"/" means home page
@main.route("/home") 
def home():
    # getting page number request when html file send page number in url_for
    page = request.args.get('page',1,type = int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 3)
    return render_template('home.html',posts = post,title = "Spiderman") # posts variable is passed having value post

@main.route("/about") #route defines webpage
#"/about" means about page
def about():
    return render_template('about.html')


