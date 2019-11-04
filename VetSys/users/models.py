from VetSys import db, login_manager, app,bc
from flask import url_for,redirect
from flask_login import UserMixin,current_user
from flask_user import UserManager
from flask_admin import Admin as Administrator, AdminIndexView,expose
from flask_admin.contrib.sqla import ModelView
from flask_user import UserManager
import datetime


@login_manager.user_loader
def user_loader(staff_id):
    return Staff.query.get(int(staff_id))


class Staff(db.Model, UserMixin):
    __name__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True);
    password = db.Column(db.String(100), nullable=False);
    #salary = db.Column(db.Float, default=db.Float(2200.5))
    #phone_number = db.Column(db.Integer)
    #name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    #address = db.Column(db.String(100))
    #start_at = db.Column(db.DateTime)
    #finish_at = db.Column(db.DateTime)
    #total_hours = db.Column(db.Interval, nullable=False, default=datetime.timedelta(hours=180))
    is_admin=db.Column(db.Boolean,default=False,nullable=False)

    def get_id(self):
        return self.staff_id

    def __repr__(self):
        return 'email: {} admin: {}'.format(self.email,self.is_admin)

    @classmethod
    def create_staff(cls,email:str,password:str,is_admin:bool):
        hashed_pass=bc.generate_password_hash(password).decode('utf-8')
        new_staff=cls(email=email,password=hashed_pass,is_admin=is_admin)
        try:
            db.session.add(new_staff)
            db.session.commit()
        except:
            return Exception('Kullanıcı oluşturulurken hata meydana geldi')







class AdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

        return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login'))


admin=Administrator(app,index_view=AdminView())
