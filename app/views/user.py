# Import flask dependencies
from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask_login import login_required, current_user

from app import db
from app.forms import UpdateProfileForm
from app.utils.decorators import check_confirmed

user = Blueprint('user', __name__, url_prefix="/post", static_folder ='static', template_folder='templates')

# Profile page
@user.route('/',methods=['POST','GET'])
@login_required
@check_confirmed
def profile():
    form = UpdateProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        current_user.firstname = form.fname.data
        current_user.lastname = form.lname.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account successfully updated","success")
        return redirect(url_for('user.profile'))

    elif request.method == 'GET':
        form.fname.data =  current_user.firstname
        form.lname.data =  current_user.lastname
        form.email.data =  current_user.email

    default_profile_img = url_for('static', filename='images/default_profile.jpg')
    return render_template("user/profile.html",
     image_file = default_profile_img, form=form)