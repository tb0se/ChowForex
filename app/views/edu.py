# Import flask dependencies
from flask import render_template, Blueprint

edu = Blueprint('edu', __name__, url_prefix="/edu",static_folder ='static',template_folder='templates')

@edu.route('/')
def index():
    return render_template("edu/index.html")