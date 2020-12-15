import sys

# Import flask dependencies
from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user

from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User


auth = Blueprint('auth', __name__, url_prefix="/auth", static_folder ='static', template_folder='templates')

# Registration
@auth.route('/register',methods=['POST','GET'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("user.profile"))

    register_form = RegistrationForm()
    # print("about to validate", file=sys.stderr)
    if request.method == 'POST' and register_form.validate_on_submit():

        # Get form data
        fname = register_form.fname.data
        lname = register_form.lname.data
        email = register_form.email.data
        password = register_form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create user
        user = User(firstname=fname, lastname=fname, email=email, password=hashed_password)
        # print(user, file=sys.stderr)

        # Save user to db
        db.session.add(user)
        db.session.commit()

        # TODO: Configure email confirmation

        flash(f'Account created for {register_form.fname.data}!', 'success')
        return redirect(url_for('auth.login'))

    return render_template("auth/register.html",form=register_form)

@auth.route('/login',methods=['POST','GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("user.profile"))

    login_form = LoginForm()

    if request.method == "POST" and login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        # check user exists
        if user and bcrypt.check_password_hash(user.password,login_form.password.data):
            login_user(user,remember=login_form.rememberMe.data)
            # retrieve the next method/page we are trying to get
            next_page = request.args.get('next')
            flash('Successfully logged in','success')
            return redirect(next_page) if next_page else redirect(url_for("user.profile"))
        else:
            flash('Incorrect username or password. Please try again.', 'danger')

    return render_template("auth/login.html",form=login_form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out','success')
    return redirect(url_for('home.index'))

# TODO: Forgot password