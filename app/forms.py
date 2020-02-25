from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User

# User Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(message = _l("Username is required."))], render_kw = {"placeholder": _l("Username")})
    password = PasswordField("Password", validators = [DataRequired(message = _l("Password is required."))], render_kw = {"placeholder": _l("Password")})
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Login"))

# User Registration Form
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(message=_l("Username is required"))], render_kw = {"placeholder": _l("Username")})
    firstName = StringField("First Name", validators = [DataRequired(message=_l("First Name is required"))], render_kw = {"placeholder": _l("First Name")})
    lastName = StringField("Last Name", validators = [DataRequired(message=_l("Last Name is required"))], render_kw = {"placeholder": _l("Last Name")})
    email = StringField("Email", validators = [DataRequired(message=_l("Username is required")), Email()], render_kw = {"placeholder": _l("Email Address")})
    password = PasswordField("Password", validators = [DataRequired(message=_l("Password is required"))], render_kw = {"placeholder": _l("Password")})
    confirm_password = PasswordField("Repeat Password", validators = [DataRequired(message=_l("Re-entry of Password is required")), EqualTo("password")], render_kw = {"placeholder": _l("Retype Password")})
    submit = SubmitField(_l("Register"))

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError(_l("Username already exists! Please use a different username."))

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError(_l("Email address already exists! Please use a different email address."))

# User Profile Edit Form
class EditProfileForm(FlaskForm):
    username = StringField(_l("Username"), validators = [DataRequired(message=_l("Username is required"))])
    firstName = StringField(_l("First Name"), validators = [DataRequired(message=_l("First Name is required"))])
    lastName = StringField(_l("Last Name"), validators = [DataRequired(message=_l("Last Name is required"))])
    submit = SubmitField(_l("Edit"))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username = self.username.data).first()
            if user is not None:
                raise ValidationError(_l("Please use a different username."))

# Reset Password Request Form
class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(message=_l("Email is required")), Email()], render_kw = {"placeholder": _l("Email Address")})
    submit = SubmitField(_l("Reset Password"))

# Password Reset Form
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators = [DataRequired(message=_l("Password is required"))], render_kw = {"placeholder": _l("Password")})
    confirmPassword = PasswordField("Confirm Password", validators = [DataRequired(message=_l("Re-Confirmation of Password is required")), EqualTo("password")], render_kw = {"placeholder": _l("Confirm Password")})
    submit = SubmitField(_l("Reset Password"))
