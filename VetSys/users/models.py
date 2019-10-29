from VetSys import db
from flask_login import UserMixin
import datetime


class Staff(db.Model, UserMixin):
    staff_id = db.Column(db.Integer, primary_key=True);
    password = db.Column(db.String(100), nullable=False);
    salary = db.Column(db.Float, default=db.Float(2200))
    phone_number = db.Column(db.Integer)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100))
    address=db.Column(db.String(100))
    free_days = db.Column(db.ARRAY(db.DateTime))
    start_at = db.Column(db.DateTime, nullable=False)
    finish_at = db.Column(db.DateTime, nullable=False)
    check_ins = db.Column(db.ARRAY(db.DateTime))
    check_outs = db.Column(db.ARRAY(db.DateTime))
    total_hours = db.Column(db.Interval, nullable=False, default=datetime.timedelta(hours=180))
