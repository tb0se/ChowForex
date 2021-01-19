from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

# Checks if user has confirmed email address
def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash("Please confirm your account!", 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def requires_role(role):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.role_allowed(role):
            flash("You do not have access to this page. Please contact your Administrator!", 'warning')
            return redirect(url_for('home.index'))
        return func(*args, **kwargs)
    return decorated_function