from sqlalchemy import String
from VetSys import db, login_manager, app, bc
from flask import url_for, redirect, flash
from flask_login import UserMixin, current_user
from flask_admin import Admin as Administrator, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
import datetime


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


# Union with
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    user_type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type
    }

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return "USER_ID: {} , USERNAME: {} , TYPE: {} ".format(self.user_id, self.username, self.user_type)

    def to_dict(self):
        return dict({'id': self.user_id, 'username': self.username, 'type': self.user_type})

    @classmethod
    def create_user(cls, username, password):
        hashed_pw = bc.generate_password_hash(password).decode('utf-8')
        new_user = cls(username=username, password=hashed_pw);

        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            return Exception("Database error")


class Admin(User):
    __tablename__ = 'admin'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    def __repr__(self):
        return super().__repr__()

    def dashboard(self):
        return "/1"

    @classmethod
    def create_user(cls, username, password):
        super().create_user(username,password)


class Assistant(User):
    __tablename__ = 'assistant'
    field = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    end_date = db.Column(db.DateTime)

    supervisor_id = db.Column(db.Integer, db.ForeignKey('vet.user_id'))

    supervisor = db.relationship('Vet', back_populates='supervisee', foreign_keys=[supervisor_id])

    __mapper_args__ = {
        "polymorphic_identity": "assistant",
    }

    def __repr__(self):
        return super().__repr__() + " FIELD: {} , END-DATE: {} ".format(self.field, self.end_date)

    def to_dict(self):
        return super().to_dict().update({'field': self.field,
                                         'end_date': self.end_date.__str__(),
                                         'supervisor': self.supervisor})


class Vet(User):
    __tablename__ = 'vet'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    field = db.Column(db.String, default='Genel uzman', nullable=False)

    # Vet supervises assistant
    supervisee = db.relationship('Assistant', foreign_keys='Assistant.supervisor_id', back_populates='supervisor')

    __mapper_args__ = {
        "polymorphic_identity": "vet",
    }

    def __repr__(self):
        return "{} FIELD: {}".format(super().__repr__(), self.field)

    def to_dict(self):
        return super().to_dict().update({'field': self.field,
                                         'end_date': self.end_date.__str__(),
                                         'supervisees': self.supervisee})

'''
class Cleaner(db.Model):
    __tablename__ = 'cleaner'
    #staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True)
    cleaning_company = db.Column(db.String, default='Caglayan pislik temizleyiciler', nullable=False)

class Secretary(db.Model):
    __tablename__ = 'secretary'
    #staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "secretary",
    }
    languages = db.relationship('Languages', backref='languages')

class Languages(db.Model):
    #staff_id = db.Column(db.Integer, db.ForeignKey('secretary.staff_id'), primary_key=True)
    language = db.Column(db.String, primary_key=True)


class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    # salary = db.Column(db.Float, ddefault=db.Float(2200.5))
    phone_number = db.Column(db.Integer)
    name = db.Column(db.String(60), nullable=False)

    address = db.Column(db.String(100))
    # start_at = db.Column(db.DateTime)
    # finish_at = db.Column(db.DateTime)
    # total_hours = db.Column(db.Interval, nullable=False, default=datetime.timedelta(hours=180))

    def __repr__(self):
        return 'email: {} admin: {}'.format(self.email, self.is_admin)


class AdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        flash('You are not allowed to enter admin section', 'error')
        return redirect(url_for('dashboard.profile'))


class UserView(ModelView):
    column_display_pk = True
    column_searchable_list = ['username']
    can_export = True
    export_types = ['csv', 'json']
    column_exclude_list = ['password']


class StaffView(ModelView):
    column_display_pk = True
    can_export = True


admin = Administrator(app, index_view=AdminView())
admin.add_view(UserView(User, db.session))
'''
