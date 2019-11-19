from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .forms import OwnerCreationForm, AppointmentCreationForm, PetCreationForm
from .models import Owner, Appointment, Pet
from VetSys import db
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
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
        return 'selam'
    return None


@dashboard.route('/make_appointment', methods=['GET', 'POST'])
@login_required
def create_appointment():
    form = AppointmentCreationForm()
    if request.method == 'GET':
        return render_template('appointment.html', form=form)

    if request.method == 'POST':
        owner = Owner.query.filter_by(name=form.owner_name.data).first()
        new_appointment = Appointment(
            appo_id=Appointment.query.filter_by().count()+1,
            on=datetime.combine(form.on.data,form.hour.data),
            appo_type=form.appointment_type.data
        )

        owner.appointments.append(new_appointment)
        db.session.add_all([owner, new_appointment])
        db.session.commit()
        flash('Appointment created succesffully')

    return render_template('appointment.html', form=form)

@dashboard.route('/register_new_pet', methods=['GET', 'POST'])
@login_required
def create_pet():
    pet_creation_form = PetCreationForm()
    if request.method == 'GET':
        return render_template('register_new_pet', pet_creation_form = pet_creation_form)

    if request.method == 'POST':
        new_pet = Pet(
            pet_name=pet_creation_form.form.pet_name.data,
            age=pet_creation_form.age.data,
            weight=pet_creation_form.weight.data,
            race=pet_creation_form.race.data,
            species=pet_creation_form.species.data,
            disabilities=pet_creation_form.disabilities.data,
        )

        db.session.add(new_pet)
        db.session.commit()
        flash('Pet entry has been created successfully!')

    return render_template('register_new_pet', pet_creation_form = pet_creation_form)

# "yeni kayit" on the left panel
@dashboard.route('/add_register', methods=['GET', 'POST'])
def add_register():
    return render_template('add_register.html')

# "kayitlari goruntule" on the left panel
@dashboard.route('/display_registers', methods=['GET', 'POST'])
def display_registers():
    return render_template('display_registers.html')
