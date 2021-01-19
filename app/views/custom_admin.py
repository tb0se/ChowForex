# Import flask dependencies
from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask import current_app as app
from flask_login import current_user, login_user, logout_user
from flask_admin import AdminIndexView, expose, helpers
from flask_admin.contrib.sqla import ModelView

from app import bcrypt
from app.forms import LoginForm
from app.models import User
from app.utils.decorators import requires_role

# Custom ModelView for Flask-admin
class CustomModelView(ModelView):
    
    # If true user can see the model
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home.index'))

# Custom AdminView for Flask-admin
class CustomAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home.index'))
        
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(CustomAdminIndexView, self).index()


    