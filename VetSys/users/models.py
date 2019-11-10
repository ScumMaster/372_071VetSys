from VetSys import db, login_manager, app, bc
from flask import url_for, redirect, flash
from flask_login import UserMixin, current_user
from flask_admin import Admin as Administrator, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
import datetime


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


# Union with
class User(db.Model, UserMixin):
    __name__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))

    def get_id(self):
        return self.user_id

    @classmethod
    def create_user(cls, username: str, password: str, is_admin: bool):
        hashed_pass = bc.generate_password_hash(password).decode('utf-8')
        new_user = cls(username=username,
                       password=hashed_pass, is_admin=is_admin)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            return Exception('Kullanıcı oluşturulurken hata meydana geldi')
        return new_user


class Assistant(db.Model):
    staff_id = db.Column(db.Integer, db.ForeignKey(
        'staff.staff_id'), primary_key=True)
    field = db.Column(db.String(60), nullable=False)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    supervisor_id = db.Column(
        db.Integer, db.ForeignKey('vet.staff_id'), nullable=False)


class Vet(db.Model):
    __name__ = 'vet'
    staff_id = db.Column(db.Integer, db.ForeignKey(
        'staff.staff_id'), primary_key=True)
    field = db.Column(db.String, default='Genel uzman', nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)

    # Vet supervises assistant
    supervisee = db.relationship('Assistant', backref='supervisor')


# class Custadion(db.Model):
# class Secretary(db.Model):

class Staff(db.Model):
    __name__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    # salary = db.Column(db.Float, ddefault=db.Float(2200.5))
    phone_number = db.Column(db.Integer)
    name = db.Column(db.String(60), nullable=False)

    address = db.Column(db.String(100))
    # start_at = db.Column(db.DateTime)
    # finish_at = db.Column(db.DateTime)
    # total_hours = db.Column(db.Interval, nullable=False, default=datetime.timedelta(hours=180))
    profile = db.relationship('User', backref='staff')

    def __repr__(self):
        return 'email: {} admin: {}'.format(self.email, self.is_admin)


class AdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        flash('You are not allowed to enter admin section', 'error')
        return redirect(url_for('users.login'))


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
