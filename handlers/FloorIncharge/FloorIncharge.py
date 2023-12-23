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
from Database.models import all_Operator_creds, all_floor_incharge, all_sites_information, gurugram_assigned_task_by_admin
from Database.init_and_conf import db

FloorIncharge1=Blueprint('FloorIncharge', __name__)



def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'})
        try:
            payload = handlers.is_token_expired(token)
            # Add the token payload to the kwargs so that it's available to the protected route
            kwargs['token_payload'] = payload
            
            if payload == False:
                # Call the original function with the token payload
                return func(*args, **kwargs)
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
        username = request.form['username']
        password = request.form['password']
        location = request.form['location']
        building_no = request.form['building_no']
        floor_no = request.form['floor_no']
        
        user = all_floor_incharge.query.filter_by(user_name = username, password = password, location = location).first()
        if user:
            return jsonify({'Response:': 'Floor_Incharge User Already Exists!'})
        else:
            new_user = all_floor_incharge(user_name=username, location=location, building_no=building_no, floor_no=floor_no, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'Response:': 'Floor_Incharge User added Successfully!'}), 401
    except:
        return jsonify({"Error": "Username or Password or location or building_no or floor_no Not Defined"}), 404


@FloorIncharge1.route("/floorincharge/login", methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        location = request.form['location']
        
        user = all_floor_incharge.query.filter_by(user_name = username, password = password, location = location).first()
        if user is not None:
            session['logged_in'] = True
            token = handlers.create_tocken(username=username, user_id = location)
            return jsonify({'Response:': 'Floor_Incharge login successfull!', 'token:': f'{token}'})
        else:
            return jsonify({'Response:': 'Authentication Failed!'}), 401
    except:
        return jsonify({"Error": "Username or Password or location Not Defined"}), 404

    
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
    token_response = handlers.create_tocken(username="example_user", user_id=123)

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


@FloorIncharge1.route("/floorincharge/operator/signup", methods=["POST"])
def operator_signup():
    try:
        username = request.form['username']
        password = request.form['password']
        mobile = request.form['mobile']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
    except:
        return jsonify({"Error": "Username and Password Not Defined"})
    
    try:
        user = all_Operator_creds.query.filter_by(email=email).first()
        if user is None:
            add_user = all_Operator_creds(username=username, password=password, mobile = mobile, email = email, first_name = first_name, last_name = last_name, dob = dob)
            db.session.add(add_user)
            db.session.commit()
            return jsonify({'Response:': "Operator User added successfully!"})
    except:
        return jsonify({"Error in adding data":"Some error occurred while adding the data to the database"})


# Floor-Incharge Dashboard all Data API
@FloorIncharge1.route("/floorincharge/dashboard")
@token_required
def dashboard(**kwargs):
    """Returns a JSON object containing all the data for floor-incharge dashboard"""
    

# On Line Number Entry Fieled Click
@FloorIncharge1.route("/floorincharge/assigntask/getline", methods=['GET'])
@token_required
def get_line(**kwargs):
    try:
        # Extract parameters from the URL
        site_location = request.args.get('site_location')
        building_no = request.args.get('building_no')
        floor_no = request.args.get('floor_no')
        
        if site_location and building_no and floor_no:
            line_data = all_sites_information.query.filter_by(site_location=site_location, building_no=building_no, floor_no=floor_no).first()
            if line_data:
                return jsonify({'line_data:': f'{type(line_data)}'})
            else:
                return jsonify({'No Data Found!':'Please add some data.'})
        else:
            return jsonify({"Error": 'Site Location, Building No., and Floor No. are required!'})
    except:
        return jsonify({"Error in getting data":"Please provide the site_location, building_no, and floor_no in parameters"}), 404


# On Part No Entry Fieled Click
@FloorIncharge1.route("/floorincharge/assigntask/getpart_no", methods=['GET'])
@token_required
def get_part_no(**kwargs):
    try:
        # Extract parameters from the URL
        building_no = request.args.get('building_no')
        floor_no = request.args.get('floor_no')
        line_no = request.args.get('line_no')
        # Get the current date and time
        current_datetime = datetime.utcnow().date()
        # Calculate one day before
        one_day_before = current_datetime - timedelta(days=1)
        part_no = gurugram_assigned_task_by_admin.query.filter_by(building_no=building_no, floor_no=floor_no, line_no = line_no, date = one_day_before).first()
        i = 2
        while part_no == False:
            one_day_before = current_datetime - timedelta(days=i)
            part_no = gurugram_assigned_task_by_admin.query.filter_by(biulding_no=building_no, floor_no=floor_no, line_no = line_no, date = one_day_before).first()
            i += 1
            
        if part_no:
            return jsonify({'get_part_no:': f'{part_no.part_number}'})
        else:
            return jsonify({'No Data Found part no!':'Please add some data.'})
    except:
        return jsonify({"Error in getting data":"Some error occurred while fetching the part no data from the database"}), 402


# Response station info after submitting the Line Number and Part Number
@FloorIncharge1.route("/floorincharge/assigntask/station_name", methods=['GET'])
@token_required
def part_no_s_process_and_operator_name(**kwargs):
    try:
        # Extract parameters from the URL
        date = request.args.get('date')
        building_no = request.args.get('building_no')
        floor_no = request.args.get('floor_no')
        line_no = request.args.get('line_no')
        part_no = request.args.get('part_no')
        
        try:
            station_info = gurugram_assigned_task_by_admin.query.filter_by(building_no=building_no, floor_no=floor_no, line_no = line_no, part_number = part_no, date = date).all()
        except Exception as e:
            print('Station_no Query Error:', e)
        
        if station_info:
            total_station_no = []
            for record in station_info:
                total_station_no.append(record.station_no)
            return jsonify({'get_station_info:': f'{total_station_no}'})
        else:
            return jsonify({'No Data Found for station info!':'Please add some data.'})
    except:
        return jsonify({"Error in getting data":"Some error occurred while fetching the station info data from the database"}), 402


# Assign Task to Operator for a part Number
@FloorIncharge1.route("/floorincharge/assigntask/assigntask", methods=['POST'])
@token_required
def change_process_and_operator_name(**kwargs):
    try:
        # Extract parameters from the URL
        date = request.form['date']
        building_no = request.form['building_no']
        floor_no = request.form['floor_no']
        line_no = request.form['line_no']
        part_no = request.form['part_no']
        process_name = request.form['process_name']
        station_no = request.form['station_no']
        app_id = request.form['app_id']
        operator_username = request.form['operator_username']
        
        assign_task = gurugram_assigned_task_by_admin.query.filter_by(date=date, station_no = station_no).first()
        
        if assign_task:
            # Update existing record
            assign_task.operator_username = operator_username
            assign_task.process_name = process_name
            db.session.commit()
            return jsonify({'Updated Successfully:': f'Operator {operator_username} has assigned process {process_name}'})
        else:
            try:
                assign_task = gurugram_assigned_task_by_admin(building_no=building_no, floor_no=floor_no, line_no = line_no, part_number = part_no, station_no = station_no, app_id = app_id, operator_username = operator_username, process_name = process_name)
                db.session.add(assign_task)
                db.session.commit()
                return jsonify({'Task Assigned Successfully:': f'Operator {operator_username} has assigned process {process_name}'})
            except Exception as e:
                print('Error ######:', e)
        
    except Exception as e:
        # An error occurred during the transaction
        print(f"Error: {str(e)}")
        db.session.rollback()
        jsonify({"Error in assigning the task": "Some error occurred while fetching the station info data from the database", 'Error is:': f'{e}'}), 402


# # Check Assigned task By App ID
# @FloorIncharge1.route('/floorincharge/checkAssignedTaskByAppId/getdata',methods=['GET'])
# @token_required
# def check_assigned_task_by_app_id(**kwargs):
#     try:
#         # Extract parameters from the URL
#         date = datetime.utcnow().date()
#         building_no = request.args.get('building_no')
#         floor_no = request.args.get('floor_no')
#         line_no = request.args.get('line_no')
#         station_no = request.args.get('station_no')
#         app_id = request.args.get('app_id')
        
#         assigned_task_to_station = assigned_task_by_admin.query.filter_by(building_no=building_no, floor_no=floor_no, date=date, station_no = station_no,  line_no = line_no, app_id = app_id).first()
        
#         if assigned_task_to_station:
#             return jsonify({'Assigned:': 'Task has Assigned to this station', 'operator_username:': f'{assigned_task_to_station.operator_username}'})
#         else:
#             return jsonify({'Not Assigned:': 'Task Has not Assigned To This Satation Yet'})
#     except Exception as e:
#         return jsonify({'Error in Try block:': f'{e}'})