from flask import Flask

# Import views
from .views.home import home

def create_app():
    """
    Create and return the Flask application
    """
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    # Register Blueprints
    app.register_blueprint(home)

    return app