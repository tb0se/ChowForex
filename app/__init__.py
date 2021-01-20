import os
import click
import logging

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask.cli import with_appcontext
from flask_mail import Mail
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app():
    """
    Create and return the Flask application
    """
    
    app = Flask(__name__, instance_relative_config=True)
    
    # Load Configuration
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
        # Logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        app.config.from_object("config.DevelopmentConfig")

    app.logger.setLevel(logging.INFO)
    # app.logger.info('ChowForex startup')


    # Initialize Flask-SQLAlchemy(db), Bcrypt, flask-migrate, Flask-Login
    # and Flask-Admin
    db.init_app(app)
    mail.init_app(app)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_user)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
       

    # Import models
    from app.models import Post, Education, User
    from app.views.custom_admin import CustomModelView, CustomAdminIndexView

    admin = Admin(app, name='Admin', template_mode='bootstrap3',
        index_view=CustomAdminIndexView()) 

    # Add Admin model views
    admin.add_view(CustomModelView(User, db.session))
    admin.add_view(CustomModelView(Post, db.session))
    admin.add_view(CustomModelView(Education, db.session))

    # Import views
    from app.views.home import home
    from app.views.auth import auth
    from app.views.user import user_bp
    from app.views.blog import blog
    from app.views.errors import errors
    from app.views.edu import edu

    # Register Blueprints
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(user_bp)
    app.register_blueprint(blog)
    app.register_blueprint(errors)
    app.register_blueprint(edu)
    

    return app


def init_db():
    """ Creates the database """
    # db.drop_all()
    db.create_all()

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

@click.command("create-user")
@with_appcontext
@click.argument("name")
def create_user(name):
    """Seeds the database with an initial admin user"""
    from app.models import User
    from flask import current_app as app
    from datetime import datetime

    admin_user = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
    if admin_user is None:
        password = bcrypt.generate_password_hash(app.config['ADMIN_PASS']).decode('utf-8')
        admin_user = User(firstname=name, lastname=name,
            email=app.config['ADMIN_EMAIL'], password=password, role='ADMIN',
            confirmed=True, confirmed_date=datetime.now()  )

        db.session.add(admin_user)
        db.session.commit()
        click.echo("Created Admin user")