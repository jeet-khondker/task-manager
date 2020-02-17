from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

# User Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(message = "Username is required.")], render_kw = {"placeholder": "Username"})
    password = PasswordField("Password", validators = [DataRequired(message = "Password is required.")], render_kw = {"placeholder": "Password"})
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

# User Registration Form
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(message="Username is required")], render_kw = {"placeholder": "Username"})
    firstName = StringField("First Name", validators = [DataRequired(message="First Name is required")], render_kw = {"placeholder": "First Name"})
    lastName = StringField("Last Name", validators = [DataRequired(message="Last Name is required")], render_kw = {"placeholder": "Last Name"})
    email = StringField("Email", validators = [DataRequired(message="Username is required"), Email()], render_kw = {"placeholder": "Email Address"})
    password = PasswordField("Password", validators = [DataRequired(message="Password is required")], render_kw = {"placeholder": "Password"})
    confirm_password = PasswordField("Repeat Password", validators = [DataRequired(message="Re-entry of Password is required"), EqualTo("password")], render_kw = {"placeholder": "Retype Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("Username already exists! Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError("Email address already exists! Please use a different email address.")

# User Profile Edit Form
class EditProfileForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(message="Username is required")])
    firstName = StringField("First Name", validators = [DataRequired(message="First Name is required")])
    lastName = StringField("Last Name", validators = [DataRequired(message="Last Name is required")])
    submit = SubmitField("Edit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username = self.username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username.")
