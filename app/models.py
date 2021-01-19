# Standard Library Imports
from datetime import datetime
import enum

# Flask Imports
from flask import current_app as app

# Local Imports
from app import db, login_manager

# 3rd party imports
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Access roles
class Role(enum.Enum):
    GUEST = 0
    USER = 1
    ADMIN = 2

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_date = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.Enum(Role), nullable=False, server_default='USER')
    posts = db.relationship('Post', backref='author', lazy=True)
    
    # Creates a new reset password token
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    # Verifies a reset password token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except :
            return None
        return User.query.get(user_id)

    # Checks if user is admin
    def is_admin(self):
        return self.role == Role.ADMIN

    # Checks if user's role is high enough
    def role_allowed(self, role):
        return self.role >= role

    def __repr__(self):
        return f'<User {self.email}>'



class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}, {self.date_posted}>'


class Education(db.Model):
    __tablename__ = 'education'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Education {self.name}>'

# Custom ModelView for Flask-admin
# class CustomModelView(ModelView):
    
#     # If true user can see the model
#     def is_accessible(self):
#         return current_user.is_authenticated

#     def inaccessible_callback(self, name, **kwargs):
#         return redirect
