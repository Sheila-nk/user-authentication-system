# User Authentication API

## Overview
This API provides user authentication functionalities, allowing users to register, login, logout, and reset their passwords. It utilizes Flask framework for building the API endpoints and SQLAlchemy for database interactions.

## Features
- **User Registration**: Users can create new accounts by providing their firstname, lastname, email, and password.
- **User Login**: Registered users can log in using their email and password.
- **User Logout**: Users can log out, which invalidates their authentication token.
- **Forgot Password**: Users can request a password reset email if they forget their password.
- **Reset Password**: Users can reset their password by following a link sent via email.

## Installation
1. Clone the repository: `git clone `
2. Navigate to the project directory: `cd user-authentication-api`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables:
   - `FLASK_APP=run.py`: Name of the Flask application
   - `FLASK_DEBUG=1`: Enable Debug mode
   - `SQLALCHEMY_DATABASE_URI`: Database URI for connecting to the database
   - `EMAIL_HOST_USER`: Email address for SMTP server authentication
   - `EMAIL_HOST_PASSWORD`: Password for SMTP server authentication
5. Initialize the database: `flask db init`
6. Create database migrations: `flask db migrate`
7. Apply migrations to the database: `flask db upgrade`
8. Run the Flask application: `flask run`

## API Endpoints
- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Log in an existing user.
- `POST /auth/logout`: Log out a user.
- `POST /auth/forgotpassword`: Request a password reset email.
- `POST /auth/resetpassword`: Reset user password.

## Usage
### Register a New User
```http
POST /auth/register
Content-Type: application/json

{
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com",
    "password": "password123"
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "password123"
}
```

### Logout
```http
POST /auth/logout
Authorization: Bearer <auth_token>
```

### Forgot Password
```http
POST /auth/forgotpassword
Content-Type: application/json

{
    "email": "john@example.com"
}
```

### Reset Password
```http
POST /auth/resetpassword
Authorization: Bearer <auth_token>
Content-Type: application/json

{
    "password": "newpassword123"
}
```

Feel free to customize this template according to your specific API implementation and requirements!