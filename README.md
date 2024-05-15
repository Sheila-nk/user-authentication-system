# User Authentication API

## Overview
This API provides user authentication functionalities, allowing users to register, login, logout, and reset their passwords. It utilizes Flask framework for building the API endpoints and SQLAlchemy for database interactions.

## Features
- **User Registration**: Users can create new accounts by providing their firstname, lastname, email, and password.
- **User Login**: Registered users can log in using their email and password.
- **User Logout**: Users can log out, which invalidates their authentication token.
- **Forgot Password**: Users can request a password reset email if they forget their password.
- **Reset Password**: Users can reset their password by following a link sent via email.

## Installation #1 (Local Development)
1. Clone the repository: 
    ```bash
    git clone https://github.com/Sheila-nk/user-authentication-system.git
    ```
2. Navigate to the project directory: 
    ```bash
    cd user-authentication-api
    ```
3. Install dependencies: 
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables 
   Refer to [.env-example](https://github.com/Sheila-nk/user-authentication-system/blob/main/.env-example) for instructions on setting up a `.env` file.

   Once created, execute the following command:
   ```bash
   source .env
   ```
5. Generate database migrations (if there are new changes to the models, otherwise skip to step 7): 
    ```bash
    flask db migrate
    ```
6. Apply migrations to the database: 
    ```bash
    flask db upgrade
    ```
7. Run the Flask application:
    ```bash
    flask run
    ```

## Installation #2 (Using Docker)
1. Clone the repository: 
    ```bash
    git clone https://github.com/Sheila-nk/user-authentication-system.git
    ```
2. Navigate to the project directory: 
    ```bash
    cd user-authentication-api
    ```
3. Build the Docker image:
    ```bash
    docker build -t user-authentication .
    ```
4. Run the Docker container:
    ```bash
    docker run -p 5001:5001 user-authentication
    ```

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