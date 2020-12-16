from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    # TODO: Look into validate maximum length with WTForm
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class AddNoteForm(FlaskForm):
    """Form for adding a note for a user."""

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])


class UpdateNoteForm(FlaskForm):
    """Form for editing a note for a user."""

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])

# TODO: create a new form for note delete button, take advantage of CSRF security
