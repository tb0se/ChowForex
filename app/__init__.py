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
    # app.config.from_mapping(
    #     SECRET_KEY ='dev',
    #     DATABASE=os.path.join(app.instance_path,'chowforex.sqlite')
    # )
    
    # Load Configuration
    # app.config.from_object('config')
    # app.config.from_pyfile('config.py')
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
        # Logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        app.config.from_object("config.DevelopmentConfig")

    app.logger.setLevel(logging.INFO)
    app.logger.info('ChowForex startup')

    #Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize Flask-SQLAlchemy(db), Bcrypt, flask-migrate and Flask-Login
    db.init_app(app)
    app.cli.add_command(init_db_command)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Flask-Mail
    mail.init_app(app)

    # Import views
    from app.views.home import home
    from app.views.auth import auth
    from app.views.user import user
    from app.views.blog import blog
    from app.views.errors import errors

    # Register Blueprints
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(user)
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