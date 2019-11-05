from VetSys import db
from datetime import datetime


class Owner(db.Model):
    __tablename__ = 'owner'
    owner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(6), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    address = db.Column(db.String(60))
    phone = db.Column(db.Integer, nullable=False, unique=True)
    # Owner makes Appointment (Weak entity)
    appointments = db.relationship('Appointment', backref='customer')
    # Owner pays Invoices
    invs = db.relationship('Invoices', backref='customer')
    # Owner owns Pet
    pets = db.relationship('Pet', backref='owner')

    def __repr__(self):
        return "id:{} name:{} sex:{} email:{} phone:{}".format(self.id, self.name, self.sex, self.email, self.phone)


''' Weak Entity in relation with Owner'''


class Appointment(db.Model):
    __tablename__ = 'appointment'
    appo_id = db.Column(db.Integer, primary_key=False)
    on = db.Column(db.DateTime, nullable=False)
    appo_type = db.Column(db.String, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), nullable=False, primary_key=True,
                         autoincrement=False)


class Invoices(db.Model):
    __tablename__ = 'invoices'
    serial_number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    cost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'))


class Cages(db.Model):
    __tablename__ = 'cages'
    cage_id = db.Column(db.Integer, nullable=False, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    emptiness = db.Column(db.Boolean, nullable=False, default=True);

    # multivalued suitability attribute
    suitabilities = db.relationship('Suitability', backref='cage')
    # multivalued notes attribute
    notes = db.relationship('CageNotes', backref='cage')


class Suitability(db.Model):
    cage_id = db.Column(db.Integer, db.ForeignKey('cages.cage_id'), primary_key=True)
    suitable = db.Column(db.String, primary_key=True)


class CageNotes(db.Model):
    cage_id = db.Column(db.Integer, db.ForeignKey('cages.cage_id'), primary_key=True)
    note = db.Column(db.String, primary_key=True)


class Pet(db.Model):
    __tablename__ = 'pet'
    pet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), default='Çomar')
    ''' Attributes inherited from Stays relation'''
    checkin_date = db.Column(db.DateTime, default=datetime.utcnow)
    checkout_date = db.Column(db.DateTime)

    specy = db.Column(db.String(60))
    race = db.Column(db.String(60))
    weight = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'))

    # multivalued notes
    notes = db.relationship('PetNotes', backref='pet')

    # multivalued disabilities
    disabilities = db.relationship('Disability', backref='pet')


class PetNotes(db.Model):
    pet = db.Column(db.Integer, db.ForeignKey('pet.pet_id'), primary_key=True)
    note = db.Column(db.String, primary_key=True)


class Disability(db.Model):
    pet = db.Column(db.Integer, db.ForeignKey('pet.pet_id'), primary_key=True)
    disab = db.Column(db.String, primary_key=True)

## cd ->

class Clinic(db.Model):
    __tablename__ = 'clinic'
    contact_info = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # clinic has medicines
    medicines = db.relationship('medicine', backref='clinic')

class Medicine(db.Model):
    __tablename__ = 'medicine'
    name = db.Column(db.String(60), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    barcode_number = db.Column(db.String(60), nullable=False, unique=True)
    serial_number = db.Column(db.String(60), nullable=False, unique=True)

    # distributor = db.Column(db.String(60), )
    # distributor has name, phone_number and email

# class Service(db.Model):
# class Accomodation(db.Model):
class Treatment(db.Model):
    _tablename_ = 'treatment'
    record_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    #has relationship?




# class Custadion(db.Model):
# class Secretary(db.Model):




