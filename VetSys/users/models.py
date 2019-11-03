from VetSys import db, login_manager,app
from flask_login import UserMixin
from flask_user import UserManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import datetime


@login_manager.user_loader
def user_loader(user_id):
    return Staff.query.get(int(user_id))




class Staff(db.Model, UserMixin):
    __name__='staff'
    staff_id = db.Column(db.Integer, primary_key=True);
    password = db.Column(db.String(100), nullable=False);
    salary = db.Column(db.Float, default=db.Float(2200))
    phone_number = db.Column(db.Integer)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100),nullable=False)
    address = db.Column(db.String(100))
    start_at = db.Column(db.DateTime, nullable=False)
    finish_at = db.Column(db.DateTime, nullable=False)
    total_hours = db.Column(db.Interval, nullable=False, default=datetime.timedelta(hours=180))

    role=db.relationship('Role',secondary='user_roles',backref='staffs')



class Role(db.Model):
    __name__='role'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True)

#User has roles (m to n)
class UserRoles(db.Model):
    __name__='user_roles'
    staff_id=db.Column(db.Integer,db.ForeignKey('staff.staff_id',ondelete='CASCADE'),primary_key=True,autoincrement=False)
    role_is=db.Column(db.Integer,db.ForeignKey('role.id',ondelete='CASCADE'),primary_key=True,autoincrement=False)


admin=Admin(app)
admin.add_view(ModelView(Staff,db.session))


