from user_authenticator import create_app, db

# The entry point of the Flask application
if __name__ == "__main__":
    # Create an instance of the Flask application using the factory function
    app = create_app()
    
    # Ensure the application context is active for database operations
    with app.app_context():
        # Create all database tables defined in the models
        db.create_all()
    
    # Run the Flask application in debug mode
    app.run(debug=True)
