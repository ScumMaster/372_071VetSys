from flask import Blueprint, render_template,flash,request
from flask_login import login_required, current_user
from .forms import OwnerCreationForm,AppointmentCreationForm
from .models import Owner,Appointment
from VetSys import db
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard')
@login_required
def profile():
    return render_template('dashboard.html')



@dashboard.route('/register_owner')
@login_required
def create_owner():
    owner_creation_form = OwnerCreationForm()
    if owner_creation_form.validate_on_submit():
        new_owner = Owner(
            name=owner_creation_form.owner_name.data,
            sex=owner_creation_form.sex.data,
            email=owner_creation_form.email.data,
            address=owner_creation_form.address,
            phone=owner_creation_form.phone
        )
        db.session.add(new_owner)
        db.session.commit()
        flash('Entry has been created successfully!')
        return None
    return None

@dashboard.route('/make_appointment',methods=['GET','POST'])
@login_required
def create_appointment():
    form=AppointmentCreationForm()
    if request.method=='GET':
        return render_template('appointment.html', form=form)
    if request.method=='POST':
        print(type(form.on.data))
        owner=Owner.query.filter_by(name=form.owner_name.data).first()
        new_appointment=Appointment(
            appo_id=Appointment.query.filter_by().count()+1,
            on=form.on.data,
            appo_type=form.appointment_type.data
        )

        owner.appointments.append(new_appointment)
        db.session.add_all([owner,new_appointment])
        db.session.commit()
        flash('Appointment created succesffully')

    return render_template('appointment.html', form=form)





