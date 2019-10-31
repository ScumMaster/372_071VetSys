from VetSys import db, login_manager
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def user_loader(user_id):
    return Staff.query.get(int(user_id))


class Staff(db.Model, UserMixin):
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





