from flask_wtf import FlaskForm
#from VetSys.users.models import Staff
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Email, Optional


class OwnerCreationForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    sex = RadioField('Sex:', choices=['Man', 'Woman'])
    phone = IntegerField('Phone:', validators=[DataRequired()])
    ssn = IntegerField('ID Number:', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    address = StringField('Address:')
    phone = IntegerField('Phone:')


class AppointmentCreationForm(FlaskForm):
    on = DateField('Date:')
    hour = TimeField('Time:')
    appointment_type = RadioField(
        'Type:', choices=[('r1', 'For once'), ('r2', 'Periodic')])
    period = StringField('Period:')
    owner_ssn = StringField('Owner SSN:')
    submit_button = SubmitField('Create')


class PetCreationForm(FlaskForm):
    pet_name = StringField('Name:')
    age = IntegerField('Age:')
    weight = IntegerField('Weight:')
    race = StringField('Race: ')
    species = StringField('Species:')
    disabilities = StringField('Disabilities:')
    owner_ssn = StringField('Owner SSN:', validators=[DataRequired()])
    submit_button = SubmitField('Create')


class TreatmentCreationForm(FlaskForm):
    treatment_type = StringField('Treatment Type:')
    start_date = DateField('Start Date:')
    end_date = DateField('End Date: ')
