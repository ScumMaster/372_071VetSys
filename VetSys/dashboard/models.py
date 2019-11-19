from VetSys import db
from datetime import datetime


class Owner(db.Model):
    __tablename__ = 'owner'
    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(5), nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    email = db.Column(db.String(60),)
    address = db.Column(db.String(60))
    # Owner makes Appointment (Weak entity)
    appointments = db.relationship('Appointment', backref='customer')
    # Owner pays Invoices
    invs = db.relationship('Invoices', backref='customer')
    # Owner owns Pet
    pets = db.relationship('Pet', backref='owner')

    def __repr__(self):
        return "id:{} name:{} sex:{} email:{} phone:{}".format(self.owner_id, self.name, self.sex, self.email, self.phone)

    @classmethod
    def create_owner(cls, owner_name, owner_sex, owner_email, owner_address, owner_phone):
        new_owner = cls(name=owner_name, sex=owner_sex,
                        email=owner_email, address=owner_address, phone=owner_phone)
        db.session.add(new_owner)
        db.session.commit()
        return new_owner


''' Weak Entity in relation with Owner'''


class Appointment(db.Model):
    __tablename__ = 'appointment'
    appo_id = db.Column(db.Integer, primary_key=True)
    on = db.Column(db.DateTime, nullable=False)
    appo_type = db.Column(db.String, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), primary_key=True,
                         autoincrement=False)


class Invoices(db.Model):
    __tablename__ = 'invoices'
    serial_number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    service_quantity = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'))
    # Invoice has service
    services = db.relationship('Service', backref='service')

class Service(db.Model):
    __tablename__ = 'service'
    name = db.Column(db.String, primary_key=True, nullable=False,autoincrement=False)
    cost = db.Column(db.Float, nullable=False)
    serial_number = db.Column(db.Integer, db.ForeignKey('invoices.serial_number'))

class Cages(db.Model):
    __tablename__ = 'cages'
    cage_id = db.Column(db.Integer, nullable=False, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    emptiness = db.Column(db.Boolean, nullable=False, default=True)

    # multivalu ed suitability attribute
    suitabilities = db.relationship('Suitability', backref='cage')
    # multivalued notes attribute
    notes = db.relationship('CageNotes', backref='cage')


class Suitability(db.Model):
    cage_id = db.Column(db.Integer, db.ForeignKey(
        'cages.cage_id'), primary_key=True)
    suitable = db.Column(db.String, primary_key=True)


class CageNotes(db.Model):
    cage_id = db.Column(db.Integer, db.ForeignKey(
        'cages.cage_id'), primary_key=True)
    note = db.Column(db.String, primary_key=True)


class Pet(db.Model):
    __tablename__ = 'pet'
    pet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), default='Çomar')
    ''' Attributes inherited from Stays relation'''
    checkin_date = db.Column(db.DateTime, default=datetime.utcnow)
    checkout_date = db.Column(db.DateTime)

    species = db.Column(db.String(60))
    race = db.Column(db.String(60))
    weight = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'))

    # multivalued disabilities
    disabilities = db.relationship('Disability')


class PetNotes(db.Model):
    pet = db.Column(db.Integer, db.ForeignKey('pet.pet_id'), primary_key=True)
    note_desc = db.Column(db.String(260), nullable=False, primary_key=True)


class Disability(db.Model):
    pet = db.Column(db.Integer, db.ForeignKey('pet.pet_id'), primary_key=True)
    disab_desc = db.Column(db.String(260), nullable=False, primary_key=True)


# cd
class Clinic(db.Model):
    __tablename__ = 'clinic'
    clinic_id = db.Column(db.Integer, primary_key=True)
    contact_info = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # clinic has medicines
    medicines = db.relationship('Medicine', backref='clinics')


class Medicine(db.Model):
    __tablename__ = 'medicine'
    serial_number = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    barcode_number = db.Column(db.String(60), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    distributor_name = db.Column(db.String(60), nullable=False)
    distributor_phone = db.Column(db.String(20), nullable=False)
    at_clinic=db.Column(db.Integer,db.ForeignKey('clinic.clinic_id'))



class Treatment(db.Model):
    _tablename_ = 'treatment'
    record_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    # has relationship?
