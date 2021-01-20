# Import flask dependencies
from flask import render_template, Blueprint

home = Blueprint('home', __name__,static_folder ='static',template_folder='templates')

# Home page
@home.route('/')
def index():
    return render_template("home/index.html")

# About Us
@home.route('/about-us/')
def about_us():
    return render_template("home/about_us.html")

# Contact Us
@home.route('/contact-us')
def contact():
    return render_template("home/contact_us.html")

# Legal
@home.route('/legal')
def legal():
    return render_template("home/legal.html")

# Brokers
@home.route('/brokers')
def brokers():
    return render_template("home/brokers.html")

# Charts
@home.route('/charts')
def charts():
    return render_template("home/charts.html")