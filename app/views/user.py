# Import flask dependencies
from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask_login import login_required

user = Blueprint('user', __name__, url_prefix="/user", static_folder ='static', template_folder='templates')

# Profile page
@user.route('/')
@login_required
def profile():
    return render_template("user/profile.html")