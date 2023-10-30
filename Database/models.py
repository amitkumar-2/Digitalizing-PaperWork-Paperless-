from init_and_conf import db
from datetime import datetime

class app_id_with_user_type(db.Model):
    app_id=db.Column(db.String(50), unique=True, nullable=False)
    user_type=db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    

class floor_incharge(db.Model):
    user_name=db.Column(db.String(30), unique=True, nullabel=False)
    location=db.Column(db.String(30), unique=True, nullabel=False)
    floor_no=db.Column(db.Integer, nullable=False)
    password=db.Column(db.String(50), nullable=False)


class UnregisterUser(db.Model):
    uid=db.Column(db.Integer, primary_key=True)
    ServTimeStemp = db.Column(db.DateTime, default=datetime.utcnow)
    mobile = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(length=40),nullable=False)
    last_name = db.Column(db.String(length=40),nullable=True)
    dob = db.Column(db.Date,nullable=True)
    otp = db.Column(db.Integer,nullable=False)
    user_type = db.Column(db.String(20))


class Operator(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=80))
    mobile = db.Column(db.String(length=14),unique=True)
    email = db.Column(db.String(length=80),unique=True)
    password = db.Column(db.String(length=80))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=None)
    first_name = db.Column(db.String(length=40))
    last_name = db.Column(db.String(length=40))
    dob = db.Column(db.Date)
