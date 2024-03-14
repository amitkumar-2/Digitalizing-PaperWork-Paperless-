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
from Database.models import Operator_creds, floor_incharge_creds, all_sites_information, gurugram_assigned_task_by_admin, all_operators_logged_in_status, work_assigned_to_operator, parts_info, processes_info, parameters_info, check_sheet_data, check_sheet_data_logs
from Database.init_and_conf import db

FloorIncharge1=Blueprint('FloorIncharge', __name__)



def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]
        else:
            token = None
        # token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'})
        try:
            payload = handlers.is_token_expired(token)
            # Add the token payload to the kwargs so that it's available to the protected route
            kwargs['token_payload'] = payload
            if payload[0] == False:
                try:
                    # Call the original function with the token payload
                    return func(*args, **kwargs)
                except:
                    return jsonify({"Error:": "An error occurred while trying to excute the function."})
            else:
                return jsonify({'Alert!': 'Token is expired!'})
        except:
            return jsonify({'Alert!': 'Invalid Token!'})
        
        
    
    return decorated

@FloorIncharge1.route('/public')
def public():
    return 'For Public FloorIncharge'

@FloorIncharge1.route('/auth')
@token_required
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
def login():
    try:
        employee_id = request.form['employee_id']
        password = request.form['password']
        
        user = floor_incharge_creds.query.filter_by(employee_id=employee_id).first()
        if user is not None:
            if user.password == password:
                session['logged_in'] = True
                token = handlers.create_tocken(employee_id=user.employee_id, mobile_no=user.mobile)
                return jsonify({'Response:': 'Floor_Incharge login successfull!', 'token:': f'{token}'}), 200
            else:
                return jsonify({'Response:': 'Authentication Failed!'}), 401
        else:
            return jsonify({'Response:': 'User Not Found!'}), 404
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

    
    # Replace the hardcoded password check with a secure authentication mechanism
    if username and password == '123456':
        session['logged_in'] = True
        token = handlers.create_tocken(username='123456', user_id = 123456)
        # handlers.decode_and_verify_token(token)
        return token
        # print("Hello world")
    else:
        return make_response('Unable to Verify', 403, {'www-Authenticate': 'Basic realm: "Authentication Failed!"'})


@FloorIncharge1.route("/generate_token")
def generate_token():
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
def FloorIncharge():
    return "<h1>This is home page</h1>"


################################### Operator signup API #######################################################
@FloorIncharge1.route("/floorincharge/operator/signup", methods=["POST"])
def operator_signup():
    try:
        employee_id = request.form['employee_id']
        fName = request.form['fName']
        try:
            mName = request.form['mName']
        except:
            mName = ''
        try:
            lName = request.form['lName']
        except:
            lName = ''
        skill_level = request.form['skill_level']
        dob = request.form['dob']
        mobile = request.form['mobile']
        email =request.form['email']
        password = request.form['password']
        
    except:
        return jsonify({"Error": "Username and Password Not Defined"})
    
    try:
        user = Operator_creds.query.filter_by(employee_id=employee_id).first()
        if user is None:
            add_user = Operator_creds(employee_id=employee_id, fName=fName, mName=mName, lName=lName, skill_level=skill_level, dob=dob, mobile=mobile, email=email, password=password)
            db.session.add(add_user)
            db.session.commit()
            return jsonify({'Response:': "Operator User added successfully!"})
        else:
            return jsonify( {"Response":"User already exists."} )
    except Exception as e:
        return jsonify({"Error in adding data":f"Some error occurred while adding the data to the database: {e}"})


# Floor-Incharge Dashboard all Data API
@FloorIncharge1.route("/floorincharge/dashboard")
@token_required
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
# @token_required
def assign_task():
    try:
        # username = kwargs["token_payload"][1]['username']
        station_id = request.form['station_id']
        employee_id = request.form['employee_id']
        part_no = request.form['part_no']
        process_no = request.form['process_no']
        start_shift_time = request.form['start_shift_time']
        end_shift_time = request.form['end_shift_time']
        shift = request.form['shift']
        assigned_by_owner = request.form['assigned_by_owner']
        
        total_assigned_task = request.form['total_assigned_task']

        # date = datetime.now().date()
        station = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
        if station:
            return jsonify({'Response': 'Please reset the all task first'})
        else:
            ####################### this data will retrieve from privious date in work_assigned_to_operator_logs table#################
            left_for_rework = 0
            assign_task_obj = work_assigned_to_operator(employee_id=employee_id, station_id=station_id, part_no=part_no, process_no=process_no, start_shift_time=start_shift_time, end_shift_time=end_shift_time, shift=shift, assigned_by_owner=assigned_by_owner, total_assigned_task=total_assigned_task, left_for_rework=left_for_rework)
            db.session.add(assign_task_obj)
            db.session.commit()
            return jsonify({'Response:': "Task assigned successfully to station!"})
        
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


######################################## add the parts with their information ###########################################
@FloorIncharge1.route("/floorincharge/add_part", methods=['POST'])
# @token_required
def add_part():
    try:
        parn_name = request.form['parn_name']
        part_no = request.form['part_no']
        added_by_owner = request.form['added_by_owner']

        exist_part_no = parts_info.query.filter_by(part_no=part_no).first()
        if exist_part_no:
            return jsonify({"Message": "This Part Number already exists."}), 200
        else:
            new_parts = parts_info(parn_name=parn_name, part_no=part_no, added_by_owner=added_by_owner)
            db.session.add(new_parts)
            db.session.commit()
            return jsonify({"Message": "New Part has been added Successfully.", "ParName": f"{parn_name}"}),  201
    
    # except Exception.IntegrityError:
    #     db.session.rollback()
    #     return jsonify({"Message": "There was a problem with your submission."}), 422
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 500
@FloorIncharge1.route("/floorincharge/get_parts", methods=[ 'GET'])
# @token_required
def get_parts():
    """Returns list of available parts"""
    try:
        data=db.session.query(parts_info.part_no, parts_info.parn_name).all()
        # print(len(data))
        # for i in range(len(data)):
        #     part_name = data[i].part_name
        #     part_no = data[i].part_no
        parts_data = [{'part_name': part_name, 'part_no': part_no} for part_name, part_no in data]
        return jsonify({"data: ": parts_data}), 200
    except Exception as e:
        return jsonify({'Error': f'Block is not able to fetch records {e}'}), 500
@FloorIncharge1.route("/floorincharge/update_part", methods=[ 'GET', 'POST'])
# @token_required
def update_part():
    try:
        part_no = request.form['part_no']
        get_part = parts_info.query.filter_by(part_no=part_no).first()
        if get_part:
            get_part.parn_name = request.form['parn_name'] or get_part.parn_name
            get_part.part_no = request.form['part_no'] or get_part.part_no
            get_part.added_by_owner = request.form.get('added_by_owner') or get_part.added_by_owner
            
            db.session.commit()
            return jsonify({"Message":"Part has been updated Successfully"}),200
        else:
            return jsonify({"Message":"No part is available"}), 404
    except Exception as e:
        return jsonify({'Error': f'Block is not able to fetch records {e}'}), 500


########################################## add the process with their information ##########################################
@FloorIncharge1.route("/floorincharge/add_process", methods=['POST'])
# @token_required
def  add_process():
    try:
        process_name = request.form['process_name']
        process_no = request.form['process_no']
        belongs_to_part = request.form['belongs_to_part']
        added_by_owner = request.form['added_by_owner']

        exist_part_no = parts_info.query.filter_by(part_no=belongs_to_part).first()
        if exist_part_no:
            exist_process_no = processes_info.query.filter_by(process_no=process_no).first()
            if exist_process_no:
                return jsonify({"Message": "This Process number already exists."})
            
            else:
                new_process = processes_info(process_name=process_name, process_no=process_no, belongs_to_part=belongs_to_part, added_by_owner=added_by_owner)
                db.session.add(new_process)
                db.session.commit()
                return jsonify({"Message": "New Process has been added Successfully.", "ProcessName": f"{process_name}"}),  201
        else:
            return jsonify({"Message":"Part does not exist."}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
@FloorIncharge1.route("/floorincharge/get_processes", methods=[ 'GET', 'POST'])
# @token_required
def get_processes():
    """Returns list of available parts"""
    try:
        part_no = request.form['part_no']
        exist_part = parts_info.query.filter_by(part_no=part_no).first()
        if exist_part:
            processes = processes_info.query.filter_by(belongs_to_part=part_no).all()
            if processes:
                print(processes[0].process_name)
                process_data = [
                    {'process_name': process.process_name, 'process_no': process.process_no}
                    for process in processes
                ]
                # print(process_data)
                return jsonify({"data: ": process_data}), 200
            else:
                return jsonify({'Message': 'No processes available for this part'}), 404
        else:
            return jsonify( {'Message':'No such Part Found.'} ), 404
    except Exception as e:
        return jsonify({'Error': f'Block is not able to fetch records {e}'}), 500


######################################## add the parameters of processes with their information ###############################
@FloorIncharge1.route("/floorincharge/add_parameter", methods=['POST'])
# @token_required
def add_parameter():
    try:
        parameter_name = request.form['parameter_name']
        parameter_no = request.form['parameter_no']
        process_no = request.form['process_no']
        belongs_to_part = request.form['belongs_to_part']
        added_by_owner = request.form['added_by_owner']
        min = request.form['min']
        max = request.form['max']
        unit = request.form['unit']
        FPA_status = request.form['FPA_status']
        
        exist_process_no = processes_info.query.filter_by(process_no=process_no).first()
        
        if exist_process_no:        
            exist_parameter_no =   parameters_info.query.filter_by(parameter_no=parameter_no).first()
            if exist_parameter_no:
                return jsonify({"Message": "This Parameters number already exists."}), 200
            
            else:
                new_process = processes_info(parameter_name=parameter_name, parameter_no=parameter_no, process_no=process_no, belongs_to_part=belongs_to_part, min=min, max=max, unit=unit, FPA_status=FPA_status, added_by_owner=added_by_owner)
                db.session.add(new_process)
                db.session.commit()
                return jsonify({"Message": "New Process has been added Successfully.", "ProcessName": f"{parameter_name}"}),  201
        else:
            return jsonify({"Message":"Process does not exist."}), 404
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


#################################################### check sheet with all information and logs  ##############################
@FloorIncharge1.route("/floorincharge/add_checksheet", methods=['POST'])
# @token_required
def add_checksheet():
    try:
        csp_id = request.form['csp_id']
        csp_name = request.form['csp_name']
        added_by_owner = request.form['added_by_owner']
        
        exist_parameter_id = check_sheet_data.query.filter_by(parameter_id=csp_id).first()
        if exist_parameter_id:
            return  jsonify({"Message": "Parameter has been already added"}), 304
        else:
            new_parameter = check_sheet_data(parameter_id=csp_id, parameter_name=csp_name, added_by_owner=added_by_owner)
            db.session.add(new_parameter)
            db.session.commit()
            return jsonify({"Message": "Data Added Successfully","Id":csp_id,"Name":csp_name}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
@FloorIncharge1.route("/floorincharge/checksheet/add_logs", methods=['POST'])
# @token_required
def checksheet_add_logs():
    try:
        csp_id = request.form['csp_id']
        oprtr_employee_id = request.form['oprtr_employee_id']
        flrInchr_employee_id = request.form['flrInchr_employee_id']
        status_datas = request.form['status_datas']
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422