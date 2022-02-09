from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterUserForm(FlaskForm):
    """Register User Form class"""

    username = StringField('User Name',
                           validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(8, 100)])
    email = StringField('Email Address',
                        validators=[InputRequired(), Length(max=50)])
    first_name = StringField('First Name',
                             validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name',
                            validators=[InputRequired(), Length(max=30)])


class LoginUserForm(FlaskForm):
    """Login the user"""

    username = StringField('User Name',
                           validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired()])


class NoteForm(FlaskForm):
    """Edits/Adds note for user"""

    title = StringField('Title',
                        validators=[InputRequired(), Length(max=100)])

    content = TextAreaField("Content",
                            validators=[InputRequired()])


class CSRFProtectForm(FlaskForm):
    """For CSRF protection"""
