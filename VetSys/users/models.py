from VetSys import db, login_manager, app, bc
from flask import url_for, redirect, flash, render_template
from flask_login import UserMixin, current_user
from flask_admin import Admin as Administrator, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import datetime
import inspect
from VetSys.dashboard import models as dmodels


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
        new_user = cls(username=username, password=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

    def user_dashboard(self, user):
        pass


class Admin(User):
    __tablename__ = 'admin'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    def __repr__(self):
        return super().__repr__()

    @classmethod
    def create_user(cls, username, password):
        super().create_user(username, password)

    def user_dashboard(self):
        return redirect('/admin')


class Assistant(User):
    __tablename__ = 'assistant'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    field = db.Column(db.String(60), nullable=False)
    end_date = db.Column(db.DateTime)

    supervisor_id = db.Column(db.Integer, db.ForeignKey('vet.user_id'))

    supervisor = db.relationship('Vet', back_populates='supervisee', foreign_keys=[supervisor_id])

    staff_id=db.Column(db.Integer,db.ForeignKey('staff.staff_id'))
    staff_t=db.relationship('Staff',back_populates='user_t',foreign_keys=[staff_id])

    __mapper_args__ = {
        "polymorphic_identity": "assistant",
    }

    # buraya supervisor ismini de ekleyelim
    def __repr__(self):
        return super().__repr__() + " FIELD: {} , END-DATE: {} ".format(self.field, self.end_date)

    def to_dict(self):
        return super().to_dict().update({'field': self.field,
                                         'end_date': self.end_date.__str__(),
                                         'supervisor': self.supervisor})

    def user_dashboard(self):
        return render_template("assistant_dashboard.html", user=self)


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

    def user_dashboard(self):
        return render_template("vet_dashboard.html", user=self)

    @classmethod
    def create_user(cls, username, password,field=None):
        hashed_pw = bc.generate_password_hash(password).decode('utf-8')
        new_user = cls(username=username, password=hashed_pw,field=field)
        db.session.add(new_user)
        db.session.commit()


class Secretary(User):
    __tablename__ = 'secretary'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "secretary",
    }




    # languages = db.relationship('Languages', backref='languages')
    # staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True)

    @classmethod
    def create_user(cls, username, password):
        super().create_user(username=username, password=password)

    def user_dashboard(self):
        return render_template("secretary_dashboard.html", user=self)


class Languages(db.Model):
    # staff_id = db.Column(db.Integer, db.ForeignKey('secretary.staff_id'), primary_key=True)
    language = db.Column(db.String, primary_key=True)


'''
class Cleaner(db.Model):
    __tablename__ = 'cleaner'
    #staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True)
    cleaning_company = db.Column(db.String, default='Caglayan pislik temizleyiciler', nullable=False)
'''

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    # salary = db.Column(db.Float, default=db.Float(2200.5))
    phone_number = db.Column(db.Integer)
    name = db.Column(db.String(60), nullable=False)

    address = db.Column(db.String(100))
    user_t = db.relationship('Assistant',back_populates='staff_t',foreign_keys='Assistant.staff_id')
    # start_at = db.Column(db.DateTime)
    # finish_at = db.Column(db.DateTime)
    # total_hours = db.Column(db.Interval, nullable=False, default=datetime.timedelta(hours=180))





class AdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.user_type == 'admin':
            return True
        return False

    def inaccessible_callback(self, **kwargs):
        flash('You are not allowed to enter admin section', 'error')
        return redirect(url_for('dashboard.profile'))


class UserView(ModelView):
    column_display_pk = True
    column_searchable_list = ['username']

    export_types = ['csv', 'json']
    column_exclude_list = ['password']
    form_edit_rules = ['user_id', 'username', 'user_type']
    form_excluded_columns = ['user_type']

    def create_model(self, form):
        form.password.data = bc.generate_password_hash(form.password.data)
        super().create_model(form)


class VetView(UserView):
    column_exclude_list = UserView.column_exclude_list[:].append('user_type')
    column_list = ['user_id', 'username', 'supervisee', 'field']


class AssistantView(UserView):
    column_exclude_list = UserView.column_exclude_list[:].append('user_type')
    column_list = ['user_id', 'username', 'supervisee', 'field','staff_t']

class SecretaryView(UserView):
    column_exclude_list = UserView.column_exclude_list[:].append('user_type')


admin = Administrator(app, index_view=AdminView())
admin.add_view(UserView(User, db.session))
admin.add_view(VetView(Vet, db.session))
admin.add_view(AssistantView(Assistant, db.session))
admin.add_view(SecretaryView(Secretary, db.session))
admin.add_view(ModelView(Staff,db.session))

for name, obj in inspect.getmembers(dmodels, inspect.isclass):
    if name != 'datetime':
        admin.add_view(ModelView(obj, db.session))
