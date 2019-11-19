from flask_wtf import FlaskForm
#from VetSys.users.models import Staff
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Email, Optional


class OwnerCreationForm(FlaskForm):
    owner_name = StringField('Name:', validators=[DataRequired()])
    sex = RadioField('Sex:', choices=['Man', 'Woman'])
    email = StringField('Email', validators=[Email()])
    address = StringField('Address:')
    phone = IntegerField('Phone:')


class AppointmentCreationForm(FlaskForm):
    on = DateField('Date:')
    hour = TimeField('Time:')
    appointment_type = RadioField(
        'Type:', choices=[('r1', 'Tek seferlik'), ('r2', 'Periyodik')])
    period = StringField('Period:')
    owner_name = StringField('Name')
    submit_button = SubmitField('Create')
