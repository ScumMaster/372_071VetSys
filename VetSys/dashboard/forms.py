from flask_wtf import FlaskForm
from VetSys.users.models import Staff
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
        'Type:', choices=[('r1', 'For once'), ('r2', 'Periodic')])
    period = StringField('Period:')
    owner_name = StringField('Name')
    submit_button = SubmitField('Create')

class PetCreationForm(FlaskForm):
    pet_name = StringField('Name:')
    age = IntegerField('Age:')
    weight = IntegerField('Weight:')
    race = StringField('Race: ')
    species = StringField('Species:')
    disabilities = StringField('Disabilities:')
    owner_name = StringField('Name:', validators=[DataRequired()])

class TreatmentCreationForm(FlaskForm):
    treatment_type = StringField('Treatment:')
    start_date = DateField('Start Date:')
    end_date = DateField('End Date: ')
