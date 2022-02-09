from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[
                           InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(max=100)])
    email = StringField("Email", validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First name", validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField("Last name", validators=[
                            InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form for logging a User into the site."""

    username = StringField("Username", validators=[
                           InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(max=100)])

class CSRFOnly(FlaskForm):
    """Form to provide CSRF protection w/o fields"""