from flask_wtf import FlaskForm
from VetSys.users.models import Staff
from wtforms import StringField,PasswordField,SubmitField,IntegerField,FloatField
from wtforms.validators import DataRequired,Email,Length

class LoginForm(FlaskForm):
    email=StringField('Email')
    password=PasswordField('Password')
    submit_button=SubmitField('Login')

class AdminLoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')