from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .forms import OwnerCreationForm, AppointmentCreationForm, PetCreationForm, TreatmentCreationForm
from .models import Owner, Appointment, Pet, Treatment
from VetSys import db
from datetime import datetime
from VetSys.decorators.route_decorators import access_granted

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def profile():
    return render_template('dashboard.html', user=current_user)

@dashboard.route('/make_appointment', methods=['GET', 'POST'])
@login_required
def create_appointment():
    form = AppointmentCreationForm()
    if request.method == 'GET':
        return render_template('appointment.html', form=form)

    if request.method == 'POST':
        owner = Owner.query.filter_by(name=form.owner_name.data).first()
        new_appointment = Appointment(
            appo_id=Appointment.query.filter_by().count() + 1,
            on=datetime.combine(form.on.data, form.hour.data),
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
    treatment_creation_form = TreatmentCreationForm()
    if request.method == 'GET':
        return render_template('register_new_pet.html', pet_creation_form=pet_creation_form,treatment_creation_form=treatment_creation_form)

    if request.method == 'POST':
        new_pet = Pet(
            name=pet_creation_form.pet_name.data,
            age=pet_creation_form.age.data,
            weight=pet_creation_form.weight.data,
            race=pet_creation_form.race.data,
            species=pet_creation_form.species.data,
            # disabilities=pet_creation_form.disabilities.data,
        )

        db.session.add(new_pet)
        db.session.commit()
        flash('Pet entry has been created successfully!')

    return render_template('register_new_pet.html', pet_creation_form=pet_creation_form,treatment_creation_form=treatment_creation_form)

@dashboard.route('/list_pet', methods=['GET', 'POST'])
@login_required
def list_pets():
    pets = Pet.query.all()
    if request.method == "POST":
        id=request.form['button-delete']
        Pet.query.filter_by(pet_id=id).delete()
        db.session.commit()
        pets = Pet.query.all()
        return render_template('list_pet.html', pets=pets)
    return render_template('list_pet.html', pets=pets)


@dashboard.route('/treatment_records', methods=['GET', 'POST'])
@login_required
def create_treatment_record():
    treatment_creation_form = TreatmentCreationForm()
    if request.method == 'GET':
        return render_template('treatment_records', treatment_creation_form=treatment_creation_form)

    if request.method == 'POST':
        new_treatment_record = Treatment(
            record_type=treatment_creation_form.treatment_type.data,
            start_date=treatment_creation_form.start_date.data,
            end_date=treatment_creation_form.end_date.data
        )

        db.session.add(new_treatment_record)
        db.session.commit()
        flash('Treatment record has been created successfully!')

    return render_template('treatment_records', treatment_creation_form=treatment_creation_form)


@dashboard.route('/create_owner', methods=['GET', 'POST'])
@login_required
def create_owner():
    create_owner_form = OwnerCreationForm()
    if request.method == 'GET':
        return render_template('create_owner', create_owner_form=create_owner_form)

    if request.method == 'POST':
        new_owner = Owner(
            name=create_owner_form.owner_name.data,
            last_name=create_owner_form.last_name.data,
            sex=create_owner_form.sex.data,
            phone=create_owner_form.phone.data,
            email=create_owner_form.email.data,
            address=create_owner_form.address.data
        )

        db.session.add(new_owner)
        db.session.commit()
        flash('Owner record has been created successfully!')

    return render_template('create_owner', create_owner_form=create_owner_form)


# "yeni kayit" on the left panel
@dashboard.route('/add_register', methods=['GET', 'POST'])
def add_register():
    return render_template('add_register.html')


# "kayitlari goruntule" on the left panel
@dashboard.route('/display_registers', methods=['GET', 'POST'])
def display_registers():
    appointments = Appointment.query.all()
    return render_template('display_registers.html', appointments=appointments)
