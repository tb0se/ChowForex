# Import flask dependencies
from flask import render_template, Blueprint

home = Blueprint('home', __name__,static_folder ='static',template_folder='templates')

# Home page
@home.route('/')
def index():
    return render_template("index.html")