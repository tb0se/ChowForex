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
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    admin = Admin(app, name='Admin', template_mode='bootstrap3')    

    # Import models
    from app.models import Post, Education, User

    # Add Admin model views
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Education, db.session))

    # Import views
    from app.views.home import home
    from app.views.auth import auth
    from app.views.user import user_bp
    from app.views.blog import blog
    from app.views.errors import errors

    # Register Blueprints
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(user_bp)
    app.register_blueprint(blog)
    app.register_blueprint(errors)
    

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