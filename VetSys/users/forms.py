from flask_wtf import FlaskForm
from VetSys.users.models import Staff
from wtforms import StringField,PasswordField,SubmitField,IntegerField,FloatField
from wtforms.validators import DataRequired,Email,Length

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit_button=SubmitField('Login')

class RegistrationForm(FlaskForm):
    email= StringField('Email',validators=[Email,DataRequired])
    password= PasswordField('Password',validators=[DataRequired])
    salary=FloatField('Salary')
    phone_number=IntegerField('Phone')
    name=StringField('Name',validators=[DataRequired])
    address=StringField('Address')
    start_at=StringField('Starting at:',validators=[Length(min(3),max(5)),DataRequired])
    finish_at=StringField('Finish at:',validators=[Length(min(3),max(5)),DataRequired])
