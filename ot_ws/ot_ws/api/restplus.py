import logging
import traceback

from flask_restplus import Api

log = logging.getLogger(__name__)

log.setLevel(logging.ERROR)

api = Api(version='1.0', title='Omnitracker API',
          description='Omnitracker API for managing Events and Tickets')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    app_settings = os.getenv('APP_SETTINGS')

    if not app_settings.FLASK_DEBUG:
        return {'message': message}, 500
