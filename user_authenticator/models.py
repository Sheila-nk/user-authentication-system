import datetime
import jwt

from flask import current_app
from sqlalchemy import Column, String, DateTime
from user_authenticator import bcrypt, db
from uuid import uuid4
from .auth.error_handling import InternalServerError

# Helper function to generate UUIDs
def get_uuid():
    return uuid4().hex

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = "users"

    # Columns for user data
    id = Column(String(32), unique=True, primary_key=True, nullable=False)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    email = Column(String(345), unique=True, nullable=False)
    password = Column(String(72), nullable=False)  # 72 characters for the hashed password
    registered_on = Column(DateTime, nullable=False)

    def __init__(self, firstname, lastname, email, password):
        # Initialize user data
        self.id = get_uuid()  # Generate a unique UUID for the user
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        # Hash the password using bcrypt with specified rounds
        self.password = bcrypt.generate_password_hash(password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.registered_on = datetime.datetime.now()

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}', '{self.registered_on}')"

    def encode_auth_token(self, user_id):
        """Generate JWT token for user authentication"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            # Encode payload into JWT token using the application's secret key
            auth_token = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return auth_token
        except Exception as e:
            # Handle encoding errors
            raise InternalServerError("Something went wrong! Our bad :(")

    @staticmethod
    def decode_auth_token(auth_token):
        """Decode JWT token for user authentication"""
        try:
            # Decode JWT token using the application's secret key
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            # Check if the token is blacklisted
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return "Token blacklisted. Please log in again."
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            # Handle invalid token
            return "Invalid token. Please log in again."

class BlacklistToken(db.Model):
    """Token model for storing JWT tokens"""
    __tablename__ = "blacklist_tokens"

    # Columns for token data
    id = Column(String(32), primary_key=True, unique=True, nullable=False)
    token = Column(String(500), unique=True, nullable=False)  # Store JWT token
    blacklisted_on = Column(DateTime, nullable=False)

    def __init__(self, token):
        # Initialize token data
        self.id = get_uuid()  # Generate a unique UUID for the token
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    @staticmethod
    def check_blacklist(auth_token):
        """Check whether a token has been blacklisted"""
        # Query the database to check if the token exists
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True  # Token is blacklisted
        return False  # Token is not blacklisted

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
