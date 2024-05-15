from marshmallow import Schema, fields, validate

class CreateSignupInputSchema(Schema):
    """
    Schema for validating user input during signup.
    
    Fields:
        firstname (str): User's first name. Minimum length is 2 characters.
        lastname (str): User's last name. Minimum length is 2 characters.
        email (str): User's email address. Must be a valid email format.
        password (str): User's password. Minimum length is 6 characters.
    """
    firstname = fields.Str(required=True, validate=validate.Length(min=2))
    lastname = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class CreateLoginInputSchema(Schema):
    """
    Schema for validating user input during login.
    
    Fields:
        email (str): User's email address. Must be a valid email format.
        password (str): User's password. Minimum length is 6 characters.
    """
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class CreateForgotPasswordSchema(Schema):
    """
    Schema for validating user input when requesting a password reset.
    
    Fields:
        email (str): User's email address. Must be a valid email format.
    """
    email = fields.Email(required=True)

class CreateResetPasswordSchema(Schema):
    """
    Schema for validating user input during password reset.
    
    Fields:
        password (str): User's new password. Minimum length is 6 characters.
    """
    password = fields.Str(required=True, validate=validate.Length(min=6))

