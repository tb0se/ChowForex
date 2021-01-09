# Import flask dependencies
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__, static_folder ='static', template_folder='templates')

# errorhandler works only for this blueprint

@errors.app_errorhandler(404)
def error_404(error):
    # app.logger.error(f'{user.email} logged in successfully')
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500