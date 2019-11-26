from VetSys import db, login_manager, app, bc
from flask import url_for, redirect, flash, render_template
from flask_login import UserMixin, current_user
from flask_admin import Admin as Administrator, AdminIndexView
from flask_admin.contrib.sqla import ModelView
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
        return "USER_ID: {} , USERNAME: {} , TYPE: {} ".format(
            self.user_id, self.username, self.user_type)

    def to_dict(self):
        return dict({'id': self.user_id,
                     'username': self.username,
                     'type': self.user_type})

    def change_password(self, password):
        self.password = bc.generate_password_hash(password).decode('utf-8')

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
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id'),
        primary_key=True)

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


class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id'),
        primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    salary = db.Column(db.Float, default=db.Float(2200.5))
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String(100))
    start_at = db.Column(db.DateTime)
    finish_at = db.Column(db.DateTime)

    assistant_t = db.relationship(
        'Assistant',
        back_populates='staff_t',
        foreign_keys='Assistant.staff_id')
    vet_t = db.relationship(
        'Vet',
        back_populates='staff_t',
        foreign_keys='Vet.staff_id')
    secretary_t = db.relationship(
        'Secretary',
        back_populates='staff_t',
        foreign_keys='Secretary.staff_id')
    cleaner_t = db.relationship(
        'Cleaner',
        back_populates='staff_t',
        foreign_keys='Cleaner.staff_id')

    __mapper_args__ = {
        "polymorphic_identity": "staff"
    }


class Assistant(User):
    __tablename__ = 'assistant'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id'),
        primary_key=True)
    field = db.Column(db.String(60), nullable=False)
    end_date = db.Column(db.DateTime)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    staff_t = db.relationship(
        'Staff',
        back_populates='assistant_t',
        foreign_keys=[staff_id])

    # end_date = db.Column(db.DateTime)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('vet.id'))
    supervisor = db.relationship(
        'Vet',
        back_populates='supervisee',
        foreign_keys=[supervisor_id])

    def user_dashboard(self):
        return render_template("assistant_dashboard.html", user=self)

    __mapper_args__ = {
        "polymorphic_identity": "assistant",
    }

    @classmethod
    def create_user(cls, username, password):
        hashed_pw = bc.generate_password_hash(password).decode('utf-8')
        new_user = cls(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()


class Vet(User):
    __tablename__ = 'vet'
    id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    field = db.Column(db.String, default='Genel uzman', nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    staff_t = db.relationship(
        'Staff',
        back_populates='vet_t',
        foreign_keys=[staff_id])
    supervisee = db.relationship(
        'Assistant',
        foreign_keys='Assistant.supervisor_id',
        back_populates='supervisor')

    appos = db.relationship(
        'Appointment',
        back_populates='assigned',
        foreign_keys='Appointment.vet_id')

    def __repr__(self):
        return "{} FIELD: {}".format(super().__repr__(), self.field)

    def to_dict(self):
        return super().to_dict().update({'field': self.field,
                                         'end_date': self.end_date.__str__(),
                                         'supervisees': self.supervisee}
                                        )

    __mapper_args__ = {
        "polymorphic_identity": "vet",
    }

    def user_dashboard(self):
        return render_template("vet_dashboard.html", user=self)

    @classmethod
    def create_user(cls, username, password, field=None):
        hashed_pw = bc.generate_password_hash(password).decode('utf-8')
        new_user = cls(username=username, password=hashed_pw, field=field)
        db.session.add(new_user)
        db.session.commit()


class Secretary(User):
    __tablename__ = 'secretary'
    id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    staff_t = db.relationship(
        'Staff',
        back_populates='secretary_t',
        foreign_keys=[staff_id])

    # languages = db.relationship('Languages', backref='languages')

    @classmethod
    def create_user(cls, username, password):
        super().create_user(username=username, password=password)

    def user_dashboard(self):
        return render_template("secretary_dashboard.html", user=self)

    __mapper_args__ = {
        "polymorphic_identity": "secretary",
    }


class Cleaner(User):
    __tablename__ = 'cleaner'
    id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    cleaning_company = db.Column(
        db.String,
        default='Caglayan pislik temizleyiciler',
        nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    staff_t = db.relationship(
        'Staff',
        back_populates='cleaner_t',
        foreign_keys=[staff_id])

    def __repr__(self):
        return 'email: {} admin: {}'.format(self.email, self.is_admin)

    @classmethod
    def create_user(cls, username, password, cleaning_company):
        cleaner = super().create_user(username=username, password=password)
        cleaner.cleaning_company = cleaning_company

    def user_dashboard(self):
        return render_template("cleaner_dashboard.html", user=self)

    __mapper_args__ = {
        "polymorphic_identity": "cleaner",
    }

    
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


class SecretaryView(UserView):
    column_exclude_list = UserView.column_exclude_list[:].append('user_type')


admin = Administrator(app, index_view=AdminView())
admin.add_view(UserView(User, db.session))
admin.add_view(VetView(Vet, db.session))
admin.add_view(AssistantView(Assistant, db.session))
admin.add_view(SecretaryView(Secretary, db.session))

for name, obj in inspect.getmembers(dmodels, inspect.isclass):
    if name != 'datetime':
        admin.add_view(ModelView(obj, db.session))
