from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from .config import ApplicationConfig

# Define a naming convention for database constraints to maintain consistency and avoid naming conflicts
convention = {
    "ix": 'ix_%(column_0_label)s',  # Index
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # Unique constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # Check constraint
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Foreign key
    "pk": "pk_%(table_name)s"  # Primary key
}

# Use the custom naming convention defined above for SQLAlchemy metadata
metadata = MetaData(naming_convention=convention)

# Initialize SQLAlchemy with custom metadata
db = SQLAlchemy(metadata=metadata)
# Initialize Bcrypt for hashing passwords
bcrypt = Bcrypt()
# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(db, render_as_batch=True)
# Initialize Flask-Mail for sending emails
mail = Mail()

def create_app(config=ApplicationConfig):
    """
    Factory function to create and configure the Flask application.

    Args:
        config (obj): Configuration object for the Flask app.

    Returns:
        app (Flask): Configured Flask application instance.
    """
    app = Flask(__name__)
    # Load configuration from the specified config object
    app.config.from_object(config)
    
    # Initialize extensions with the Flask app instance
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Import and register the authentication blueprint and error handlers
    from user_authenticator.auth.views import auth_blueprint
    from user_authenticator.auth.error_handling import register_error_handlers

    # Register the authentication blueprint with a URL prefix
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # Register custom error handlers
    register_error_handlers(app)

    return app
