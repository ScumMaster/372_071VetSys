from flask_wtf import FlaskForm
from VetSys.users.models import Staff
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email

class LoginForm(FlaskForm):
    staff_id=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit_button=SubmitField('Login')