from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app.models import User

# User Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(message = "Username is required.")])
    password = PasswordField("Password", validators = [DataRequired(message = "Password is required.")])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")