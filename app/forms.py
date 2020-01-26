from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

# User Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(message = "Username is required.")])
    password = PasswordField("Password", validators = [DataRequired(message = "Password is required.")])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

# User Registration Form
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(message="Username is required")])
    email = StringField("Email", validators = [DataRequired(message="Username is required"), Email()])
    password = PasswordField("Password", validators = [DataRequired(message="Password is required")])
    confirm_password = PasswordField("Repeat Password", validators = [DataRequired(message="Re-entry of Password is required"), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("Username already exists! Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError("Email address already exists! Please use a different email address.")