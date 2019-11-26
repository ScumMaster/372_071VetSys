from flask_wtf import FlaskForm
# from VetSys.users.models import Staff
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Login')


class VetForm(FlaskForm):
    name = StringField('Name:')
    surname = StringField('Last Name:')
    password = PasswordField('Password', validators=[DataRequired])
    e_mail = StringField('E-mail:')
    field = StringField('Field:')
    phone_number = StringField('Phone Number: ')
