from Database.init_and_conf import db
from datetime import datetime

class app_id_with_user_type(db.Model):
    app_id=db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    user_type=db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    

class floor_incharge(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(30), unique=True)
    location=db.Column(db.String(30), nullable=False)
    building_no = db.Column(db.String(30), nullable = False)
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


class Operator_creds(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=80), unique=True)
    mobile = db.Column(db.String(length=14),unique=True)
    email = db.Column(db.String(length=80),unique=True)
    password = db.Column(db.String(length=80))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=None)
    first_name = db.Column(db.String(length=40))
    last_name = db.Column(db.String(length=40))
    dob = db.Column(db.Date)
    app_id = db.Column(db.String(length=20))


class sites_information(db.Model):
    site_id = db.Column(db.Integer, primary_key=True)
    site_location = db.Column(db.String(length=25), nullable=False)
    building_no = db.Column(db.String(length=16), nullable=False)
    floor_no = db.Column(db.String(length=16), nullable=False)
    line_no = db.Column(db.String(length=16), nullable=False)
    station_no = db.Column(db.String(length=16), nullable=False)


class part_no_and_name_info(db.Model):
    part_id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(length=16), nullable=False)
    part_name = db.Column(db.String(length=36), nullable=False)
    process_name = db.Column(db.String(length=100), nullable=False)


# We will create this table for every building
class assigned_task_by_admin(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(length=16), nullable=False)
    process_name = db.Column(db.String(length=100), nullable=False)
    building_no = db.Column(db.String(length=16), nullable=False)
    floor_no = db.Column(db.String(length=16), nullable=False)
    line_no = db.Column(db.String(length=16), nullable=False)
    app_id = db.Column(db.String(length=20), nullable=False)
    station_no = db.Column(db.String(length=20), nullable=False)
    operator_username = db.Column(db.String(length=80), nullable=False)
    assigned_time = db.Column(db.DateTime, default=datetime.utcnow())
    date = db.Column(db.Date, default=datetime.utcnow().date())


class operators_logged_in_status(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    operator_username = db.Column(db.String(length=80), nullable=False)
    mobile = db.Column(db.String(length=14),nullable = False)
    line_no = db.Column(db.String(length=16), nullable=False)
    station_no = db.Column(db.String(length=20), nullable=False)
    login_status = db.Column(db.Boolean, default = False)