from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

from .forms import OwnerCreationForm, AppointmentCreationForm, PetCreationForm, TreatmentCreationForm, \
    MedicineCreationForm
from .models import Owner, Appointment, Pet, Treatment, Medicine
from VetSys.users.forms import VetForm
from VetSys.users.models import User
from VetSys import db
from datetime import datetime
from VetSys.decorators.route_decorators import access_granted

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def profile():
    return current_user.user_dashboard()


@dashboard.route('/create_owner', methods=['GET', 'POST'])
@login_required
def create_owner():
    owner_creation_form = OwnerCreationForm()
    if request.method == 'GET':
        return render_template('create_owner.html', owner_creation_form=owner_creation_form)

    if request.method == 'POST':
        if owner_creation_form.validate_on_submit():
            new_owner = Owner(
                ssn=owner_creation_form.ssn.data,
                name=owner_creation_form.name.data,
                last_name=owner_creation_form.last_name.data,
                sex=owner_creation_form.sex.data,
                phone=owner_creation_form.phone,
                email=owner_creation_form.email.data,
                address=owner_creation_form.address
            )
            db.session.add(new_owner)
            db.session.commit()
            flash('Owner added successfully!')
    return None


@dashboard.route('/make_appointment', methods=['GET', 'POST'])
@login_required
def create_appointment():
    form = AppointmentCreationForm()
    owner_form = OwnerCreationForm()
    if request.method == 'GET':
        return render_template('appointment.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            owner = Owner.query.filter_by(ssn=form.owner_ssn.data).first()
            new_appointment = Appointment(
                owner_ssn=owner.ssn,
                appo_id=Appointment.query.filter_by().count() + 1,
                on=datetime.combine(form.on.data, form.hour.data),
                appo_type=form.appointment_type.data
            )
            current_user.appos.append(new_appointment)

            owner.appointments.append(new_appointment)

            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment created succesffully')

    return render_template('appointment.html', form=form, owner_form=owner_form)


@dashboard.route('/register_new_pet', methods=['GET', 'POST'])
@login_required
def register_new_pet():
    pet_creation_form = PetCreationForm()
    treatment_creation_form = TreatmentCreationForm()
    if request.method == 'GET':
        return render_template('register_new_pet.html', pet_creation_form=pet_creation_form,
                               treatment_creation_form=treatment_creation_form)

    if request.method == 'POST':
        if treatment_creation_form.validate_on_submit():
            add_list = []
            pet_q = Pet.query.filter_by(name=pet_creation_form.pet_name.data).first()
            if pet_q is None:
                pet_q = Pet(
                    name=pet_creation_form.pet_name.data,
                    age=pet_creation_form.age.data,
                    weight=pet_creation_form.weight.data,
                    race=pet_creation_form.race.data,
                    species=pet_creation_form.species.data,
                    # disabilities=pet_creation_form.disabilities.data,
                )
                ow_t=Owner.query.filter_by(ssn=pet_creation_form.owner_ssn.data).first()
                ow_t.pets.append(pet_q)

                add_list.append(pet_q)


            new_treatment = Treatment(
                record_type=treatment_creation_form.treatment_type.data,
                start_date=treatment_creation_form.start_date.data,
                end_date=treatment_creation_form.start_date.data,
            )

            add_list.append(new_treatment)

            pet_q.treatments.append(new_treatment)
            db.session.add_all(add_list)
            db.session.commit()
            flash('Pet entry has been created successfully!')

    return render_template('register_new_pet.html',user=current_user,pet_creation_form=pet_creation_form,
                           treatment_creation_form=treatment_creation_form)


@dashboard.route('/list_pet', methods=['GET', 'POST'])
@login_required
def list_pet():
    pets = Pet.query.all()
    if request.method == "POST":
        id = request.form['button-delete']
        Pet.query.filter_by(pet_id=id).delete()
        db.session.commit()
        pets = Pet.query.all()
        return render_template('list_pet.html', pets=pets)
    return render_template('list_pet.html', pets=pets)


@dashboard.route('/delete_pet', methods=['GET'])
@login_required
def delete_pet():
    pet_id = request.args['button-delete']
    temp_pet = Pet.query.filter_by(pet_id=pet_id)
    Pet.query.filter_by(pet_id=pet_id).delete()
    db.session.commit()
    return jsonify({'msg': "{} has been deleted.".format(temp_pet.name)})


@dashboard.route('/treatment_records', methods=['GET', 'POST'])
@login_required
def create_treatment_record():
    treatment_creation_form = TreatmentCreationForm()
    if request.method == 'GET':
        return render_template('treatment_records.html', treatment_creation_form=treatment_creation_form)

    if request.method == 'POST':
        if treatment_creation_form.validate_on_submit():
            new_treatment_record = Treatment(
                record_type=treatment_creation_form.treatment_type.data,
                start_date=treatment_creation_form.start_date.data,
                end_date=treatment_creation_form.end_date.data
            )
            # burayi bi duzeltsenize ya henuz legit olmamis - cagatay
            pet = Pet.query.filter_by(name=treatment_creation_form.pet_name.data).first()
            pet.treatments.append(new_treatment_record)
            db.session.add_all([new_treatment_record, pet])
            db.session.commit()
            flash('Treatment record has been created successfully!')

    return render_template('treatment_records', treatment_creation_form=treatment_creation_form)


@dashboard.route('/display_registers', methods=['GET', 'POST'])
@login_required
def display_registers():
    appointments = current_user.appos
    if request.method == "POST":
        id = request.form['button-delete']
        Appointment.query.filter_by(appo_id=id).delete()
        db.session.commit()
        appointments = Appointment.query.all()
        return render_template('display_registers.html', appointments=appointments)

    return render_template('display_registers.html', appointments=appointments)


@dashboard.route('/search_pet', methods=['POST'])
@login_required
def search_pet():
    if request.form['text'] == "":
        return jsonify({})
    pets = Pet.query.filter(Pet.name.like("%" + request.form['text'] + "%")).all()
    results = [p.to_dict() for p in pets]
    return jsonify({'query': results})


@dashboard.route('/search_owner', methods=['POST'])
@login_required
def search_owner():
    if request.form['text'] == "":
        return jsonify({})
    owners = Owner.query.filter(Owner.name.like("%" + request.form['text'] + "%")).all()
    results = [o.to_dict() for o in owners]
    return jsonify({'query': results})


@dashboard.route('/delete_appointment', methods=['GET'])
@login_required
def delete_appointment():
    appo_id = request.args['button-delete']
    temp_appo = Appointment.query.filter_by(appo_id=appo_id)
    Appointment.query.filter_by(appo_id=appo_id).delete()
    db.session.commit()
    return jsonify({'msg': "{} has been deleted.".format(temp_appo.appo_id)})


@dashboard.route('/profile', methods=['GET', 'POST'])
@login_required
def profile2():
    vet = VetForm()
    user = current_user.query.filter_by().first()
    # user.query.all()
    return render_template('profile.html', user=user, vet=vet)


@dashboard.route('/add_medicine', methods=['GET', 'POST'])
@login_required
def add_medicine():
    medicine_form = MedicineCreationForm()
    if request.method == 'GET':
        return render_template('add_medicine.html', medicine_form=medicine_form)

    if request.method == 'POST':
        if medicine_form.validate_on_submit():
            new_medicine = Medicine(
                serial_number=medicine_form.serial_number.data,
                name=medicine_form.name.data,
                barcode_number=medicine_form.barcode_number.data,
                expiration_date=medicine_form.expiration_date.data,
                distributor_name=medicine_form.distributor_name.data,
                distributor_phone=medicine_form.distributor_phone.data,
            )
            db.session.add(new_medicine)
            db.session.commit()
            flash('Treatment record has been created successfully!')

    return render_template('add_medicine.html', medicine_form=medicine_form)


@dashboard.route('/display_medicine', methods=['GET', 'POST'])
@login_required
def display_medicine():
    medicines = Medicine.query.group_by(Medicine.name).all()
    quantity = []
    for q in medicines:
        quantity.append(Medicine.query.filter_by(name=q.name).count())

    if request.method == 'GET':
        return render_template('/display_medicine.html', medicines=medicines, quantity=quantity)
