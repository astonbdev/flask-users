from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length, URL, Optional


class RegisterUserForm(FlaskForm):
    """Register User Form class"""
    username = StringField('User Name',
                           validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(8)])
    email = StringField('Email Address',
                        validators=[InputRequired()])
    first_name = StringField('First Name',
                             validators=[InputRequired()])
    last_name = StringField('Last Name',
                            validators=[InputRequired()])

class LoginUserForm(FlaskForm):
    """Login the user"""
    username = StringField('User Name',
                           validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired()])