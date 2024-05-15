import os
from flask import jsonify
from flask_mail import Message
from sqlalchemy import exc
from user_authenticator import db, bcrypt, mail
from .error_handling import BadRequest, ResourceNotFound, Unauthorized, InternalServerError
from .validation import CreateSignupInputSchema, CreateLoginInputSchema, CreateForgotPasswordSchema, CreateResetPasswordSchema
from ..models import User, BlacklistToken

def create_user(request, post_data):
    """
    Creates a user if one does not already exist.
    
    Args:
        request (Request): The HTTP request object.
        post_data (dict): The JSON data from the request containing user details.
        
    Returns:
        response (Response): JSON response with a success message and status code.
    """
    signupschema = CreateSignupInputSchema()
    errors = signupschema.validate(post_data)
    if errors:
        raise BadRequest(errors)
    
    user = User.query.filter_by(email=post_data.get("email")).first()
    if user:
        raise BadRequest("User already exists. Please log in.")
    
    try:
        user = User(**post_data)
        db.session.add(user)
        db.session.commit()
        responseObject = {'message': 'User registered successfully.'}
        response = jsonify(responseObject)
        response.status_code = 201
        return response
    except exc.IntegrityError as uq:
        raise BadRequest("User already exists. Please log in.")
    except Exception as e:
        raise InternalServerError("Something went wrong! Our bad :(")

def login_user(request, post_data):
    """
    Logs in a registered user.
    
    Args:
        request (Request): The HTTP request object.
        post_data (dict): The JSON data from the request containing login details.
        
    Returns:
        response (Response): JSON response with user details and auth token, or an error message.
    """
    login_schema = CreateLoginInputSchema()
    errors = login_schema.validate(post_data)
    if errors:
        raise BadRequest(errors)
    
    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        raise ResourceNotFound("User does not exist. Please create an account.")
    if not bcrypt.check_password_hash(user.password, post_data.get('password')):
        raise Unauthorized("Invalid password. Try again.")
    
    try:
        auth_token = user.encode_auth_token(user.id)
        responseObject = {
            'auth_token': str(auth_token),
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
        }
        response = jsonify(responseObject)
        response.status_code = 200
        return response               
    except Exception as e:
        raise InternalServerError("Something went wrong! Our bad :(")

def logout_user(request, auth_header):
    """
    Logs out a user by blacklisting the JWT token.
    
    Args:
        request (Request): The HTTP request object.
        auth_header (str): The authorization header containing the JWT token.
        
    Returns:
        response (Response): JSON response with a success message.
    """
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            raise BadRequest("Bearer token malformed")
    else:
        auth_token = ''
    
    if auth_token:
        response = User.decode_auth_token(auth_token)
        user = User.query.filter_by(id=response).first()
        if not user:
            raise Unauthorized(response)
        
        blacklist_token = BlacklistToken(token=auth_token)
        try:
            db.session.add(blacklist_token)
            db.session.commit()
            responseObject = {'message': 'Successfully logged out'}
            response = jsonify(responseObject)
            response.status_code = 200
            return response
        except Exception as e:
            raise InternalServerError("Something went wrong! Our bad :(")

def send_reset_password_email(request, user):
    """
    Sends a password reset email to the user.
    
    Args:
        request (Request): The HTTP request object.
        user (User): The user object.
        
    Returns:
        token (str): The JWT token generated for password reset.
    """
    mail_subject = "Reset Your Password"
    domain = request.base_url
    uid = user.id
    token = user.encode_auth_token(uid)
    message = Message(
        mail_subject, sender=os.environ.get("EMAIL_HOST_USER"), recipients=[user.email]
    )
    message.html = f"Please click on the link to reset your password, {domain}/pages/auth/reset-password/{uid}/{token}"
    
    try:
        mail.send(message)
        return token
    except Exception as e:
        raise InternalServerError("Something went wrong!")

def forgot_password(request, post_data):
    """
    Handles the forgot password process by sending a reset link to the user's email.
    
    Args:
        request (Request): The HTTP request object.
        post_data (dict): The JSON data from the request containing the user's email.
        
    Returns:
        response (Response): JSON response with a success message and auth token.
    """
    forgot_password_schema = CreateForgotPasswordSchema()
    errors = forgot_password_schema.validate(post_data)
    if errors:
        raise BadRequest(errors)
    
    user = User.query.filter_by(email=post_data.get("email")).first()
    if not user:
        raise BadRequest("User does not exist. Please create an account.")
    
    try:
        auth_token = send_reset_password_email(request, user)
        responseObject = {
            'auth_token': str(auth_token),
            'message': 'Link to reset password successfully sent'
        }
        response = jsonify(responseObject)
        response.status_code = 200
        return response
    except Exception as e:
        raise InternalServerError("Something went wrong! Check your network connection then try again.")

def reset_password(request, input_data, auth_header):
    """
    Resets the user's password using the token provided in the authorization header.
    
    Args:
        request (Request): The HTTP request object.
        input_data (dict): The JSON data from the request containing the new password.
        auth_header (str): The authorization header containing the JWT token.
        
    Returns:
        response (Response): JSON response with a success message.
    """
    reset_password_schema = CreateResetPasswordSchema()
    errors = reset_password_schema.validate(input_data)
    if errors:
        raise BadRequest(errors)
    
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            raise BadRequest("Bearer token malformed")
    else:
        raise BadRequest("Token is required!")
    
    response = User.decode_auth_token(auth_token)
    user = User.query.filter_by(id=response).first()
    if not user:
        raise Unauthorized(response)
    
    try:
        password = bcrypt.generate_password_hash(input_data.get('password'))
        user.password = password.decode()
        # Blacklist auth token after it has been used to reset the user's password
        blacklist_token = BlacklistToken(token=auth_token)
        db.session.add(blacklist_token)
        db.session.commit()
        responseObject = {'message': 'Password has been reset successfully'}
        response = jsonify(responseObject)
        response.status_code = 201
        return response
    except Exception as e:
        raise InternalServerError("Something went wrong! Our bad :(")
