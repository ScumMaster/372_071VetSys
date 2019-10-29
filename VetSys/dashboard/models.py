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
    invs=db.relationship('Invoices',backref='customer')
    # Owner owns Pet
    pets=db.relationship('Pet',backref='owner')

    def __repr__(self):
        return "id:{} name:{} sex:{} email:{} phone:{}".format(self.id, self.name, self.sex, self.email, self.phone)

''' Weak Entity in relation with Owner'''
class Appointment(db.Model):
    __tablename__ = 'appointment'
    appo_id = db.Column(db.Integer, primary_key=False)
    on = db.Column(db.DateTime, nullable=False)
    appo_type = db.Column(db.String, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), nullable=False, primary_key=True, autoincrement=False)


class Invoices(db.Model):
    __tablename__ = 'invoices'
    serial_number=db.Column(db.Integer,primary_key=True,autoincrement=False)
    cost=db.Column(db.Float,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    total_price=db.Column(db.Float,nullable=False)
    transaction_date=db.Column(db.DateTime,nullable=False)

    owner_id=db.Column(db.Integer,db.ForeignKey('owner.owner_id'))



class Cages(db.Model):
    __tablename__ = 'cages'
    cage_id = db.Column(db.Integer, nullable=False, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    suitability = db.Column(db.ARRAY(db.String()), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.ARRAY(db.String()))
    emptiness = db.Column(db.Boolean, nullable=False, default=True);

class Pet(db.Model):
    __tablename__='pet'
    pet_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(60),default='Çomar')
    notes=db.Column(db.ARRAY(db.String))
    ''' Attributes inherited from Stays relation'''
    checkin_date=db.Column(db.DateTime,default=datetime.utcnow)
    checkout_date=db.Column(db.DateTime)

    disabilities=db.Column(db.ARRAY(db.String))
    specy=db.Column(db.String(60))
    race=db.Column(db.String(60))
    weight=db.Column(db.Float,nullable=False)
    age=db.Column(db.Integer,nullable=False)

    owner_id=db.Column(db.Integer,db.ForeignKey('owner.owner_id'))





