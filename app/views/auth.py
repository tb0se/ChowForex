# Import flask dependencies
from flask import render_template, Blueprint, request, url_for, redirect, flash
import sys

from app.forms import RegistrationForm, LoginForm
from app.models import User,db

from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__, url_prefix="/auth", static_folder ='static', template_folder='templates')

# Registration
@auth.route('/register',methods=['POST','GET'])
def register():

    register_form = RegistrationForm()
    # print("about to validate", file=sys.stderr)
    if request.method == 'POST' and register_form.validate_on_submit():
        # Check that email does not already exist in db

        # user = User(register_form.fname.data, register_form.lname.data,register_form.email.data,register_form.password.data)
        # print(user, file=sys.stderr)

        # Save user to db
        # db.session.add(user)
        # db.session.commit()

        # Configure email confirmation

        # flash('Thanks for registering')
        flash(f'Account created for {register_form.fname.data}!', 'success')
        return redirect(url_for('auth.login'))

    return render_template("auth/register.html",form=register_form)

@auth.route('/login',methods=['POST','GET'])
def login():
    login_form = LoginForm()

    if request.method == "POST" and login_form.validate_on_submit():

        if login_form.email == "test@email.com" and login_form.password == "test":

            flash('You have been logged in!', 'success')
            return redirect(url_for("user.profile"))

        else:
            flash('Incorrect username or password. Please try again.', 'danger')

    return render_template("auth/login.html",form=login_form)

# TODO: Forgot password