from Database.init_and_conf import db
from datetime import datetime
import pytz

# class app_id_with_user_type(db.Model):
#     app_id=db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
#     user_type=db.Column(db.String(20), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
    

############################# companies all floor In-Charge Info ########################################
class floor_incharge_creds(db.Model):
    # id=db.Column(db.Integer, autoincrement=True)
    employee_id=db.Column(db.String(30), unique=True, primary_key=True)
    location=db.Column(db.String(30), nullable=False)
    building_no = db.Column(db.String(30), nullable = False)
    floor_no=db.Column(db.String(length=10), nullable=False)
    fName = db.Column(db.String(length=15), nullable=False)
    mName = db.Column(db.String(length=15))
    lName = db.Column(db.String(length=15))
    dob = db.Column(db.Date)
    mobile = db.Column(db.String(length=14),unique=True)
    email = db.Column(db.String(length=80),unique=True)
    password=db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))


# class UnregisterUser(db.Model):
#     uid=db.Column(db.Integer, primary_key=True)
#     ServTimeStemp = db.Column(db.DateTime, default=datetime.now())
#     mobile = db.Column(db.String(50), nullable=False)
#     first_name = db.Column(db.String(length=40),nullable=False)
#     last_name = db.Column(db.String(length=40))
#     dob = db.Column(db.Date,nullable=True)
#     otp = db.Column(db.Integer,nullable=False)
#     user_type = db.Column(db.String(20))


############################# companies all operators Info ########################################
class Operator_creds(db.Model):
    # id = db.Column(db.Integer, autoincrement=True)
    employee_id = db.Column(db.String(length=20), unique=True, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
    fName = db.Column(db.String(length=15), nullable=False)
    mName = db.Column(db.String(length=15))
    lName = db.Column(db.String(length=15))
    skill_level = db.Column(db.String(length=10)) # 0 - beginner
    dob = db.Column(db.Date)
    mobile = db.Column(db.String(length=14),unique=True)
    email = db.Column(db.String(length=80),unique=True)
    password = db.Column(db.String(length=80), nullable=False)


# class all_operators_logged_in_status(db.Model):
#     log_id = db.Column(db.Integer, primary_key=True)
#     operator_username = db.Column(db.String(length=80), nullable=False)
#     mobile = db.Column(db.String(length=14),nullable = False)
#     # line_no = db.Column(db.String(length=16), nullable=False)
#     station_no = db.Column(db.String(length=20), nullable=False)
#     login_status = db.Column(db.Boolean, default = False)
#     first_login_time = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
#     last_login_time = db.Column(db.Date)
#     logout_time = db.Column(db.Date)
#     date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())


# class all_sites_information(db.Model):
#     site_id = db.Column(db.Integer, primary_key=True)
#     site_location = db.Column(db.String(length=25), nullable=False)
#     building_no = db.Column(db.String(length=16), nullable=False)
#     floor_no = db.Column(db.String(length=16), nullable=False)
#     line_no = db.Column(db.String(length=16), nullable=False)
#     station_no = db.Column(db.String(length=16), nullable=False)


# class all_part_no_and_name_info(db.Model):
#     part_id = db.Column(db.Integer, primary_key=True)
#     part_number = db.Column(db.String(length=16), nullable=False)
#     part_name = db.Column(db.String(length=36), nullable=False)
#     process_name = db.Column(db.String(length=100), nullable=False)


# We will create this table for every building
# class gurugram_assigned_task_by_admin(db.Model):
#     task_id = db.Column(db.Integer, primary_key=True)
#     part_number = db.Column(db.String(length=16), nullable=False)
#     process_name = db.Column(db.String(length=100), nullable=False)
#     building_no = db.Column(db.String(length=16), nullable=False)
#     floor_no = db.Column(db.String(length=16), nullable=False)
#     line_no = db.Column(db.String(length=16), nullable=False)
#     app_id = db.Column(db.String(length=20), nullable=False)
#     station_no = db.Column(db.String(length=20), nullable=False)
#     operator_username = db.Column(db.String(length=80), nullable=False)
#     assigned_time = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
#     date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())




# class gurugram_line_performance(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     line_no = db.Column(db.String(length=20), nullable=True)
#     target = db.Column(db.String(length=15))
#     passed = db.Column(db.String(length=15))
#     failed = db.Column(db.String(length=15))
#     filled = db.Column(db.String(length=15))
#     date_time = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
#     date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())


# class gurugram_station_performance(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sift = db.Column(db.String(length=10), nullable=False)
#     station_no = db.Column(db.String(length=20), nullable=False)
#     target = db.Column(db.String(length=15))
#     passed = db.Column(db.String(length=15))
#     failed = db.Column(db.String(length=15))
#     filled = db.Column(db.String(length=15))
#     date_time = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
#     date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())



################################# companies all stations info ##########################################
class stations(db.Model):
    # id = db.Column(db.Integer, autoincrement=True)
    station_id = db.Column(db.String(length=25), unique=True, primary_key=True)
    line_no = db.Column(db.String(length=20), nullable=False)
    floor_no = db.Column(db.String(length=20), nullable=False)
    building_no = db.Column(db.String(length=10), nullable=False)
    location = db.Column(db.String(length=25), nullable=False)
    added_by_owner = db.Column(db.String(length=15), nullable=False)
    added_time = db.Column(db.Time, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
    added_date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())


################################# work assigned to operator table ######################################
class work_assigned_to_operator(db.Model):
    # id = db.Column(db.Integer, autoincrement=True)
    employee_id = db.Column(db.String(length=20), nullable=False, unique=True)
    station_id = db.Column(db.String(length=15), primary_key=True, nullable=False)
    part_no = db.Column(db.String(length=20), nullable=False)
    process_no = db.Column(db.String(length=20), nullable=False, unique=True)
    start_shift_time = db.Column(db.Time, nullable=False)
    end_shift_time = db.Column(db.Time, nullable=False)
    shift = db.Column(db.String(length=2), nullable=False)
    assigned_by_owner = db.Column(db.String(30), nullable=False)
    operator_login_status = db.Column(db.Boolean, default=False)  # True means the operator is logged in
    total_assigned_task = db.Column(db.Integer, nullable=False)
    left_for_rework = db.Column(db.Integer)
    passed = db.Column(db.Integer)
    filled = db.Column(db.Integer)
    failed = db.Column(db.Integer)
    time = db.Column(db.Time, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())

class work_assigned_to_operator_logs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(length=20), nullable=False, index=True)
    station_id = db.Column(db.String(length=15), nullable=False, index=True)
    part_no = db.Column(db.String(length=20), nullable=False)
    process_no = db.Column(db.String(length=20), nullable=False)
    start_shift_time = db.Column(db.Time, nullable=False)
    end_shift_time = db.Column(db.Time, nullable=False)
    shift = db.Column(db.String(length=2), nullable=False)
    assigned_by_owner = db.Column(db.String(30), nullable=False)
    total_assigned_task = db.Column(db.Integer, nullable=False)
    left_for_rework = db.Column(db.Integer)
    passed = db.Column(db.Integer)
    filled = db.Column(db.Integer)
    failed = db.Column(db.Integer)
    time = db.Column(db.Time, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())


##################################### all parts information table #########################################
class parts_info(db.Model):
    # id = db.Column(db.Integer, autoincrement=True)
    part_name = db.Column(db.String(length=64), nullable=False)
    part_no = db.Column(db.String(length=20), primary_key=True)
    added_by_owner = db.Column(db.String(30), nullable=False)
    disabled = db.Column(db.Boolean, default=False)
    time = db.Column(db.Time, default=datetime.now().time())
    date = db.Column(db.Date, default=datetime.now().date())


###################################### all process name information table ##################################
class  processes_info(db.Model):
    # id = db.Column(db.Integer, autoincrement=True)
    process_name = db.Column(db.String(length=220), nullable=False)
    process_no = db.Column(db.String(length=40), primary_key=True)
    belongs_to_part = db.Column(db.String(length=20), nullable=False)
    images_urls = db.Column(db.String(length=1200))
    added_by_owner = db.Column(db.String(30), nullable=False)
    time = db.Column(db.Time, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())


#################### all parameters information table or Set Up and First Part Approval######################
class parameters_info(db.Model):
    # id = db.Column(db.Integer, autoincrement=True)
    parameter_name = db.Column(db.String(length=220), nullable=False)
    parameter_no = db.Column(db.String(length=60), primary_key=True)
    process_no = db.Column(db.String(length=40), nullable=False)
    belongs_to_part = db.Column(db.String(length=20), nullable=False)
    min = db.Column(db.String(length=15))
    max = db.Column(db.String(length=15))
    unit = db.Column(db.String(length=20))
    FPA_status = db.Column(db.Boolean, default=False)
    readings_is_available = db.Column(db.Boolean, default=False)
    added_by_owner = db.Column(db.String(30), nullable=False)
    time = db.Column(db.Time, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())

class  fpa_and_set_up_approved_records(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operator_employee_id = db.Column(db.String(length=20), nullable=False, index=True)
    start_shift_1_parameters_values = db.Column(db.String(length=1500))
    start_shift_1_time = db.Column(db.Time)
    start_shift_2_parameters_values = db.Column(db.String(length=1500))
    start_shift_2_time = db.Column(db.Time)
    end_shift_1_parameters_values = db.Column(db.String(length=1500))
    end_shift_1_time = db.Column(db.Time)
    end_shift_2_parameters_values = db.Column(db.String(length=1500))
    end_shift_2_time = db.Column(db.Time)
    date = db.Column(db.Date, nullable=False, index=True)

class  fpa_and_set_up_approved_records_logs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operator_employee_id = db.Column(db.String(length=20), nullable=False)
    start_shift_1_parameters_values = db.Column(db.String(length=50))
    start_shift_1_time = db.Column(db.Time)
    start_shift_2_parameters_values = db.Column(db.String(length=50))
    start_shift_2_time = db.Column(db.Time)
    end_shift_1_parameters_values = db.Column(db.String(length=50))
    end_shift_1_time = db.Column(db.Time)
    end_shift_2_parameters_values = db.Column(db.String(length=50))
    end_shift_2_time = db.Column(db.Time)
    date = db.Column(db.Date, nullable=False)



#################################### all stations information logs ##########################################
# class station_info_logs(db.Model):
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     station_id = db.Column(db.String(length=15), nullable=False)
#     total_assigned_task = db.Column(db.Integer, nullable=False)
#     left_for_rework = db.Column(db.Integer)
#     passed = db.Column(db.Integer)
#     filled = db.Column(db.Integer)
#     failed = db.Column(db.Integer)
#     start_shift_timing = db.Column(db.Time, nullable=False)
#     end_shift_timing = db.Column(db.Time, nullable=False)
#     date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())

# class station_info(db.Model):
#     # id = db.Column(db.Integer, autoincrement=True)
#     station_id = db.Column(db.String(length=15), primary_key=True)
#     total_assigned_task = db.Column(db.Integer, nullable=False)
#     left_for_rework = db.Column(db.Integer)
#     passed = db.Column(db.Integer)
#     filled = db.Column(db.Integer)
#     failed = db.Column(db.Integer)
#     start_shift_timing = db.Column(db.Time, nullable=False)
#     end_shift_timing = db.Column(db.Time, nullable=False)
#     date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())


########################################################### Startup check sheet data ######################################################
class check_sheet(db.Model):
    csp_id = db.Column(db.Integer, primary_key=True)
    csp_name = db.Column(db.String(length=300), nullable=False)
    csp_name_hindi = db.Column(db.String(length=250))
    specification = db.Column(db.String(length=300))
    control_method = db.Column(db.String(length=80))
    frequency = db.Column(db.String(length=80))
    added_by_owner = db.Column(db.String(length=30), nullable=False)
    time = db.Column(db.Time, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())

class check_sheet_data(db.Model):
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # csp_id = db.Column(db.String(length=15), nullable=False) # Check Sheet Parameter Id
    station_id = db.Column(db.String(length=15), primary_key=True)
    oprtr_employee_id = db.Column(db.String(length=20), unique=True)  # Operator Employee ID
    flrInchr_employee_id = db.Column(db.String(length=30))
    status_datas = db.Column(db.String(length=1500), nullable=False)
    time = db.Column(db.Time, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())

class check_sheet_data_logs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # csp_id = db.Column(db.String(length=15), nullable=False) # Check Sheet Parameter Id
    station_id = db.Column(db.String(length=15), nullable=False, index=True)
    oprtr_employee_id = db.Column(db.String(length=20), nullable=False, index=True)  # Operator Employee ID
    flrInchr_employee_id = db.Column(db.String(length=30))
    status_datas = db.Column(db.String(length=1500), nullable=False)
    time = db.Column(db.Time, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())



############################################## table to get reading status for parameters ##################################
class reading_params(db.Model):
    parameter_no = db.Column(db.String(length=60), primary_key=True)
    reading_1 = db.Column(db.String(length=10))
    reading_1_time = db.Column(db.Time)
    reading_2 = db.Column(db.String(length=10))
    reading_2_time = db.Column(db.Time)
    reading_3 = db.Column(db.String(length=10))
    reading_3_time = db.Column(db.Time)
    reading_4 = db.Column(db.String(length=10))
    reading_4_time = db.Column(db.Time)
    reading_5 = db.Column(db.String(length=10))
    reading_5_time = db.Column(db.Time)
    operator_employee_id = db.Column(db.String(length=20), nullable=False)
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())

class reading_params_logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parameter_no = db.Column(db.String(length=60), nullable=False)
    reading_1 = db.Column(db.String(length=10), nullable=False)
    reading_1_time = db.Column(db.Time, nullable=False)
    reading_2 = db.Column(db.String(length=10), nullable=False)
    reading_2_time = db.Column(db.Time, nullable=False)
    reading_3 = db.Column(db.String(length=10), nullable=False)
    reading_3_time = db.Column(db.Time, nullable=False)
    reading_4 = db.Column(db.String(length=10), nullable=False)
    reading_4_time = db.Column(db.Time, nullable=False)
    reading_5 = db.Column(db.String(length=10), nullable=False)
    reading_5_time = db.Column(db.Time, nullable=False)
    operator_employee_id = db.Column(db.String(length=20), nullable=False)
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())



################################################## UCL and LCL table for params #######################################
class params_ucl_lcl(db.Model):
    parameter_no = db.Column(db.String(length=60), primary_key=True)
    UCL = db.Column(db.Float)
    LCL = db.Column(db.Float)
    time = db.Column(db.Time, default=datetime.now(pytz.timezone('Asia/Kolkata')).time())
    date = db.Column(db.Date, default=datetime.now(pytz.timezone('Asia/Kolkata')).date())



######################################## operator check params notification table ####################################
class  notify_to_incharge(db.Model):
    station_id = db.Column(db.String(length=25), primary_key=True)
    csp_id = db.Column(db.Integer, primary_key=True)
    floor_no = db.Column(db.String(length=15), nullable=False)
    created_at = db.Column(db.DateTime)