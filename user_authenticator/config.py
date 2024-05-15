from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class ApplicationConfig:
    # Secret key for protecting against CSRF attacks and session tampering
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Disable tracking modifications to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Echo SQL statements to the console for debugging purposes
    SQLALCHEMY_ECHO = True

    # Database URI, which should be set in the environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # Set the complexity of the encryption (12 rounds is a common choice)
    BCRYPT_LOG_ROUNDS = 12

    # Enable debugging mode for the Flask application
    DEBUG = True

    # Configuration for the email server
    MAIL_SERVER = "smtp.gmail.com"  # Example: Gmail SMTP server
    MAIL_PORT = 587  # TLS port for SMTP
    MAIL_USERNAME = os.environ.get('EMAIL_HOST_USER')  # Email username
    MAIL_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # Email password
    MAIL_USE_TLS = True  # Use TLS for secure communication with the SMTP server
    MAIL_USE_SSL = False  # Do not use SSL (TLS should be used instead)

    # Additional configurations can be added as needed
