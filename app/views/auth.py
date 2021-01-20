import sys
from datetime import datetime

# Import flask dependencies
from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask import current_app as app
from flask_login import login_user, current_user, logout_user, login_required

from app import db, bcrypt, mail
from app.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from app.models import User

from flask_mail import Message
from app.utils.email import send_email

auth = Blueprint('auth', __name__, url_prefix="/auth", static_folder ='static', template_folder='templates')

# Registration
@auth.route('/register',methods=['POST','GET'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("user_bp.profile"))

    register_form = RegistrationForm()
    # print("about to validate", file=sys.stderr)
    if request.method == 'POST' and register_form.validate_on_submit():

        # Get form data
        fname = register_form.fname.data
        lname = register_form.lname.data
        uname = register_form.uname.data
        email = register_form.email.data
        password = register_form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create user
        user = User(firstname=fname, lastname=lname, username=uname,
                email=email, password=hashed_password,
                confirmed=False)
        # print(user, file=sys.stderr)

        # Save user to db
        db.session.add(user)
        db.session.commit()

        # Email confirmation
        email_token = user.get_reset_token()
        confirm_url = url_for('auth.confirm_email', token=email_token, _external=True)
        html = render_template('auth/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email address"
        send_email(user.email, subject, html)

        flash(f'Account created for {register_form.fname.data}!', 'success')
        return redirect(url_for('auth.login'))
        # return redirect(url_for('auth.unconfirmed'))

    return render_template("auth/register.html",form=register_form)


# Email Confirmation
@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):

    user = User.verify_reset_token(token)

    if user is None:
        flash('The confirmation link is invalid or has expired.','danger')
        return redirect(url_for('auth.resend_confirmation'))

    if user.confirmed:
        flash('Account already confirmed. Please login.','success')
    else:
        user.confirmed = True
        user.confirmed_date = datetime.now()
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home.index'))


# Remind users to confirm emails
@auth.route('/unconfirmed')
# @login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for("user_bp.profile"))
    # flash('Please confirm your account!','warning')
    return render_template('auth/unconfirmed.html')

# Resend confirmation email
@auth.route('/resend')
@login_required
def resend_confirmation():
    email_token = current_user.get_reset_token()
    confirm_url = url_for('auth.confirm_email', token=email_token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email address"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.','success')
    return redirect(url_for('home.index'))

# Login
@auth.route('/login',methods=['POST','GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("user_bp.profile"))

    login_form = LoginForm()

    if request.method == "POST" and login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        # check user exists
        if user and bcrypt.check_password_hash(user.password,login_form.password.data):

            login_user(user, remember = login_form.rememberMe.data)
            app.logger.info(f'{user.email} logged in successfully')

            # retrieve the next method/page we are trying to get
            next_page = request.args.get('next')
            flash('Successfully logged in','success')
            # return redirect(next_page) if next_page else redirect(url_for("user.profile"))
            return redirect(next_page) if next_page else redirect(url_for("home.index"))
            
        else:
            if user :
                app.logger.info(f'{user.email} failed to login')
            flash('Incorrect username or password. Please try again.', 'danger')

    return render_template("auth/login.html",form=login_form)


# Logout
@auth.route('/logout')
def logout():
    logout_user()
    # app.logger.info(f'{user.email} logged out successfully')
    flash('Successfully logged out','success')
    return redirect(url_for('home.index'))

# Send reset emails
def send_reset_email(user):
    token = user.get_reset_token()

    # Construct email
    subject_line = 'Password Reset Request'
    sender = 'noreply@demo.com'
    msg = Message(subject_line,
        sender=sender, 
        recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{ url_for('auth.reset_token', token=token, _external=True) }

If you did not make this request then simply igonre this email and no changes will be made.
'''
    mail.send(msg)

# Request to reset password
@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():

    if current_user.is_authenticated:
        # return redirect(url_for("user.profile"))
        return redirect(url_for("home.index"))

    request_reset_form = RequestResetForm()

    if request.method == "POST" and request_reset_form.validate_on_submit():
        user = User.query.filter_by( email=request_reset_form.email.data ).first()
        send_reset_email(user)
        flash('Email has been sent with intstuctions to reset password.','info')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_request.html', form=request_reset_form)


# Actually reset the password with token active
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        # return redirect(url_for("user.profile"))
        return redirect(url_for("home.index"))

    user = User.verify_reset_token(token)

    if user is None:
        flash("Invalid/Expired token.","warning")
        return redirect(url_for('auth.reset_request'))

    reset_password_form = ResetPasswordForm()
    if request.method == 'POST' and reset_password_form.validate_on_submit():

        # Get form data
        password = reset_password_form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user.password = hashed_password
        db.session.commit()

        flash(f'Password has been updated', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_token.html', form=reset_password_form)


