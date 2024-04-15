# from flask import Blueprint, render_template

# home=Blueprint('home', __name__)

# @home.route("/floor-incharge-home")
# @home.route("/")
# def floorInchargeHome():
#     return "<h1>This is home page</h1>"



from flask import Blueprint, render_template, request, session, jsonify, make_response
import handlers
from datetime import datetime, timedelta
from functools import wraps
from collections import Counter
from Database.models import Operator_creds, floor_incharge_creds, work_assigned_to_operator, parts_info, processes_info, parameters_info, check_sheet_data, check_sheet_data_logs, work_assigned_to_operator_logs
import pytz
from Database.init_and_conf import db
from Models.FloorIncharge.FloorIncharge import login, operator_signup, add_part, get_parts, update_part, add_process, get_processes, add_parameter, add_checksheet, stations_info, stations_current_status, refresh_data, free_stations_if_task_completed, disable_part, assign_task, update_processes, update_parameter, get_parameter, get_notification_info, get_floor_data
from Config.token_handler import TokenRequirements

FloorIncharge1=Blueprint('FloorIncharge', __name__)



# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         auth_header = request.headers.get('Authorization')
#         if auth_header and auth_header.startswith('Bearer '):
#             token = auth_header.split(" ")[1]
#         else:
#             token = None
#         # token = request.args.get('token')
#         if not token:
#             return jsonify({'Alert!': 'Token is missing!'})
#         try:
#             payload = handlers.is_token_expired(token)
#             # Add the token payload to the kwargs so that it's available to the protected route
#             kwargs['token_payload'] = payload
#             if payload[0] == False:
#                 try:
#                     # Call the original function with the token payload
#                     return func(*args, **kwargs)
#                 except:
#                     return jsonify({"Error:": "An error occurred while trying to excute the function."})
#             else:
#                 return jsonify({'Alert!': 'Token is expired!'})
#         except:
#             return jsonify({'Alert!': 'Invalid Token!'})
        
        
    
#     return decorated

@FloorIncharge1.route('/public')
def public():
    return 'For Public FloorIncharge'

@FloorIncharge1.route('/auth')
@TokenRequirements.token_required
def auth(**kwargs):
    return 'JWT is verified. Welcome to your Dashboard!'
# def auth(**kwargs):
#     token_payload = kwargs.get('token_payload')
#     print("##################", token_payload)
    
#     # Check if the token payload is available
#     if token_payload == False:
#         # return jsonify({'message': f'JWT is verified. Welcome to your Dashboard, {token_payload["user"]}!'})
#         return jsonify({'message': f'JWT is verified. Welcome to your Dashboard, {token_payload}!'})
#     else:
#         # The decorator has already handled the case where the token is missing or invalid
#         # This line will not be reached if the token is missing or invalid
#         return jsonify({'message': 'Authentication failed.'}), 401


# Home
@FloorIncharge1.route("/")
def home():
    if not session.get('logged_in'):
        return jsonify({'response': 'Not Logged In'})
    else:
        return jsonify({'response': 'Logged In'})


@FloorIncharge1.route("/floorincharge/signup", methods=['POST'])
def signup():
    try:
        employee_id = request.form['employee_id']
        location = request.form['location']
        building_no = request.form['building_no']
        floor_no = request.form['floor_no']
        fName = request.form['fName']
        try:
            mName = request.form['mName']
        except Exception as e:
            mName = ''
        try:
            lName = request.form['lName']
        except Exception as e:
            lName = ''
        dob = request.form['dob']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        
        user = floor_incharge_creds.query.filter_by(employee_id=employee_id).first()
        if user:
            return jsonify({'Response:': 'Floor_Incharge User Already Exists!'}), 200
        else:
            new_user = floor_incharge_creds(employee_id=employee_id, location=location, building_no=building_no, floor_no=floor_no, fName=fName, mName=mName, lName=lName, dob=dob, mobile=mobile, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'Response:': 'Floor_Incharge User added Successfully!'}), 201
    except:
        return jsonify({"Error in adding data":f"Some error occurred while adding the data to the database: {e}"}), 500


@FloorIncharge1.route("/floorincharge/login", methods=['POST'])
def login_handler(**kwargs):
    return login(request.form)



@FloorIncharge1.route("/generate_token")
def generate_token(**kwargs):
    # Generate the token using your create_token function
    token_response = handlers.create_tocken(employee_id="example_user", mobile_no=123)

    # Extract the token from the response
    # token = token_response.get_json().get('token')

    # Now you can pass the token to decode_and_verify_token
    # decoded_token = handlers.decode_and_verify_token(token)
    
    # Now you can pass the token to decode_and_verify_token
    expired_token = handlers.is_token_expired(token_response)
    # print(expired_token)

    # Handle the decoded token as needed

    # return "Token generated and decoded successfully!"
    return expired_token

@FloorIncharge1.route("/floorincharge")
def FloorIncharge(**kwargs):
    return "<h1>This is home page</h1>"


################################### Operator signup API #######################################################
@FloorIncharge1.route("/floorincharge/operator/signup", methods=["POST"])
def operator_signup_handler():
    return operator_signup(request.form)


# Floor-Incharge Dashboard all Data API
@FloorIncharge1.route("/floorincharge/dashboard")
@TokenRequirements.token_required
def dashboard(**kwargs):
    try:
        """Returns a JSON object containing all the data for floor-incharge dashboard"""
        username = kwargs["token_payload"][1]['username']
        date = datetime.now().date()
        user = floor_incharge_creds.query.filter_by(user_name=username).first()
        if user:
            location = user.location
            building_no = user.building_no
            floor_no = user.floor_no
            
            try:
                get_login_users_status = all_operators_logged_in_status.query.filter_by(date=date, login_status=True).all()
                print('##########', get_login_users_status)
                active_stations = len(get_login_users_status)
                get_line_and_station_no = all_sites_information.query.filter_by(site_location = location, building_no = building_no, floor_no = floor_no).all()
                list_total_line = []
                for i in range(len(get_line_and_station_no)):
                    line = get_line_and_station_no[i].line_no
                    list_total_line.append(line)
                    
                stations_at_one_line = dict(Counter(list_total_line))
                total_line = set(list_total_line)
                
                
                return jsonify({'username': f'{username}', 'total_line': f'{len(total_line)}', 'total_stations': f'{len(get_line_and_station_no)}', 'total_stations_at_one_line': f'{stations_at_one_line}', 'active_stations': f'{active_stations}'})
            except:
                return jsonify({'Error': 'Unable to get line no and station no information'})
    except:
        return jsonify({'Error': 'Block is not able to execute successfully'}), 422


############ assign task to stations one by one using this api ###########################
@FloorIncharge1.route("/floorincharge/assign_task", methods=['POST'])
# @TokenRequirements.token_required
def assign_task_handler(**kwargs):
    return assign_task(request.json)


######################################## add the parts with their information ###########################################
@FloorIncharge1.route("/floorincharge/add_part", methods=['POST'])
@TokenRequirements.token_required
def add_part_handler(**kwargs):
    return add_part(request.form)
@FloorIncharge1.route("/floorincharge/get_parts", methods=[ 'GET'])
@TokenRequirements.token_required
def get_parts_handler(**kwargs):
    return get_parts()
@FloorIncharge1.route("/floorincharge/update_part", methods=[ 'GET', 'POST'])
@TokenRequirements.token_required
def update_part_handler(**kwargs):
    return update_part(request.form)
@FloorIncharge1.route("/floorincharge/disable_part", methods=['POST'])
@TokenRequirements.token_required
def disable_part_handler(**kwargs):
    return disable_part(request.form)


########################################## add the process with their information ##########################################
@FloorIncharge1.route("/floorincharge/add_process", methods=['POST'])
@TokenRequirements.token_required
def  add_process_handler(**kwargs):
    return add_process(request.form, request.files)
@FloorIncharge1.route("/floorincharge/get_processes", methods=[ 'GET', 'POST'])
@TokenRequirements.token_required
def get_processes_handler(**kwargs):
    return get_processes(request.form)

@FloorIncharge1.route("/floorincharge/update_processes", methods=[ 'GET', 'POST'])
@TokenRequirements.token_required
def update_processes_handler(**kwargs):
    return update_processes(request.form)


######################################## add the parameters of processes with their information ###############################
@FloorIncharge1.route("/floorincharge/add_parameter", methods=['POST'])
@TokenRequirements.token_required
def add_parameter_handler(**kwargs):
    return add_parameter(request.form)

@FloorIncharge1.route("/floorincharge/get_parameter", methods=['POST'])
@TokenRequirements.token_required
def get_parameter_handler(**kwargs):
    return get_parameter(request.form)

@FloorIncharge1.route("/floorincharge/update_parameter", methods=['POST'])
@TokenRequirements.token_required
def update_parameter_handler(**kwargs):
    return update_parameter(request.form)


#################################################### check sheet with all information and logs  ##############################
@FloorIncharge1.route("/floorincharge/add_checksheet", methods=['POST'])
@TokenRequirements.token_required
def add_checksheet_handler(**kwargs):
    return add_checksheet(request.form)
@FloorIncharge1.route("/floorincharge/checksheet/add_logs", methods=['POST'])
@TokenRequirements.token_required
def checksheet_add_logs(**kwargs):
    try:
        csp_id = request.form['csp_id']
        oprtr_employee_id = request.form['oprtr_employee_id']
        flrInchr_employee_id = request.form['flrInchr_employee_id']
        status_datas = request.form['status_datas']
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


####################################################### getting staions info #######################################################
@FloorIncharge1.route("/floorincharge/stations_info", methods=['POST'])
@TokenRequirements.token_required
def stations_info_hendler(**kwargs):
    return stations_info(request.form)

########################################## getting staions current status #######################################
@FloorIncharge1.route("/floorincharge/stations_current_status", methods=['GET'])
@TokenRequirements.token_required
def stations_current_status_handler(**kwargs):
    return stations_current_status()


########################################## refresh stations static information #######################################
@FloorIncharge1.route("/floorincharge/refresh_data", methods=['POST'])
@TokenRequirements.token_required
def refresh_data_handler(**kwargs):
    return refresh_data(request.json)

################################################### get FPA history ############################################




############################################### free stations if task is completed ######################################
@FloorIncharge1.route("/floorincharge/free_station", methods=['POST'])
@TokenRequirements.token_required
def free_station(**kwargs):
    return free_stations_if_task_completed(request.json)


############################################# get notification info ############################################
@FloorIncharge1.route("/floorincharge/get_notifications", methods=['POST'])
@TokenRequirements.token_required
def get_notification_info_handler(**kwargs):
    return get_notification_info(request.form)

############################################# get floor all data ############################################
@FloorIncharge1.route("/floorincharge/get_floor_data", methods=['POST'])
@TokenRequirements.token_required
def get_floor_data_handler(**kwargs):
    return get_floor_data(request.form)