from flask import Blueprint, request
from flask.views import MethodView

from .users import create_user, login_user, logout_user, forgot_password, reset_password

# Define a blueprint for authentication-related routes
auth_blueprint = Blueprint('auth', __name__)

# Class-based view for user registration
class RegisterAPI(MethodView):
    """
    Sets up the Registration route for a new user.
    Handles POST requests to create a new user.
    """
    def post(self):
        post_data = request.get_json()  # Get JSON data from the request
        response = create_user(request, post_data)  # Call the create_user function
        return response

# Create a view function for the RegisterAPI and add it to the blueprint
registration_view = RegisterAPI.as_view('register_api')
auth_blueprint.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST']
)

# Class-based view for user login
class LoginAPI(MethodView):
    """
    Sets up the Login route for a registered user.
    Handles POST requests to authenticate a user.
    """
    def post(self):
        post_data = request.get_json()  # Get JSON data from the request
        response = login_user(request, post_data)  # Call the login_user function
        return response

# Create a view function for the LoginAPI and add it to the blueprint
login_view = LoginAPI.as_view('login_api')
auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)

# Class-based view for user logout
class LogoutAPI(MethodView):
    """
    Sets up the Logout route that blacklists the JWT token.
    Handles POST requests to log out a user and blacklist their token.
    """
    def post(self):
        auth_header = request.headers.get('Authorization')  # Get the Authorization header
        response = logout_user(request, auth_header)  # Call the logout_user function
        return response

# Create a view function for the LogoutAPI and add it to the blueprint
logout_view = LogoutAPI.as_view('logout_api')
auth_blueprint.add_url_rule(
    '/logout',
    view_func=logout_view,
    methods=['POST']
)

# Class-based view for forgot password functionality
class ForgotPasswordAPI(MethodView):
    """
    Sets up the Forgot Password route.
    Handles POST requests to initiate a password reset.
    """
    def post(self):
        post_data = request.get_json()  # Get JSON data from the request
        response = forgot_password(request, post_data)  # Call the forgot_password function
        return response

# Create a view function for the ForgotPasswordAPI and add it to the blueprint
forgotpassword_view = ForgotPasswordAPI.as_view('forgotpassword_api')
auth_blueprint.add_url_rule(
    '/forgotpassword',
    view_func=forgotpassword_view,
    methods=['POST']
)

# Class-based view for reset password functionality
class ResetPasswordAPI(MethodView):
    """
    Sets up the Reset Password route.
    Handles POST requests to reset the user's password.
    """
    def post(self):
        auth_header = request.headers.get('Authorization')  # Get the Authorization header
        input_data = request.get_json()  # Get JSON data from the request
        response = reset_password(request, input_data, auth_header)  # Call the reset_password function
        return response

# Create a view function for the ResetPasswordAPI and add it to the blueprint
resetpassword_view = ResetPasswordAPI.as_view('resetpassword_api')
auth_blueprint.add_url_rule(
    '/resetpassword',
    view_func=resetpassword_view,
    methods=['POST']
)
