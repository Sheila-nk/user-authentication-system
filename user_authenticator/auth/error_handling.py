"""
This module implements custom exception types and installs error handlers
for them that produce the errors in the format the user is expecting.
For more information, visit: https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
"""

from flask import jsonify

class BadRequest(Exception):
    """Custom Exception to be thrown when a local error occurs."""
    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class Unauthorized(Exception):
    """Custom Exception to be thrown when the user is unauthorized."""
    def __init__(self, message, status_code=401, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class Forbidden(Exception):
    """Custom Exception to be thrown when access is forbidden."""
    def __init__(self, message, status_code=403, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class ResourceNotFound(Exception):
    """Custom Exception to be thrown when the requested resource is not found."""
    def __init__(self, message, status_code=404, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class InternalServerError(Exception):
    """Custom Exception to be thrown for unexpected server-side errors."""
    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

def register_error_handlers(app):
    """
    Registers error handlers for custom exceptions with the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.errorhandler(BadRequest)
    @app.errorhandler(Unauthorized)
    @app.errorhandler(Forbidden)
    @app.errorhandler(ResourceNotFound)
    @app.errorhandler(InternalServerError)
    def handle_exception(error):
        """
        Handles the custom exceptions and returns a JSON response.

        Args:
            error (Exception): The custom exception instance.

        Returns:
            response (Response): A JSON response with the error details and status code.
        """
        payload = dict(error.payload or ())
        payload['status_code'] = error.status_code
        payload['message'] = error.message
        return jsonify(payload), error.status_code
