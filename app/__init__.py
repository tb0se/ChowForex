import os
import click

from flask import Flask
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

# Load database
from app.models import db

# Import models
# from .models import User

def create_app():
    """
    Create and return the Flask application
    """
    
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY ='dev',
    #     DATABASE=os.path.join(app.instance_path,'chowforex.sqlite')
    # )
    
    # Load Configuration
    # app.config.from_object('config')
    # app.config.from_pyfile('config.py')
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    #Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize Flask-SQLAlchemy and the init-db command
    db.init_app(app)
    app.cli.add_command(init_db_command)
    # with app.app_context():
    #     db.create_all()
    # app.app_context().push()
    # db.create_all()


    # Flask login settings
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view =  "signin"

    # @login_manager.user_loader
    # def load_user(userid):
    #     return User.query.filter(User.id==userid).first()


    # Import views
    from app.views.home import home
    from app.views.auth import auth
    from app.views.user import user

    # Register Blueprints
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(user)

    return app


def init_db():
    db.drop_all()
    db.create_all()

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")