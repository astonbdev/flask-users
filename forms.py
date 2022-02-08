from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, URL, Optional

class RegisterUserForm(FlaskForm):
    """Register User Form class"""