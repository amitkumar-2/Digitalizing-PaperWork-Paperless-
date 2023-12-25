from flask import Blueprint, render_template, request, session, jsonify, make_response
import handlers
from datetime import datetime, timedelta
from functools import wraps
from Database.models import all_Operator_creds, all_floor_incharge, all_sites_information, gurugram_assigned_task_by_admin, all_operators_logged_in_status
from Database.init_and_conf import db

Operator1=Blueprint('Operator', __name__)



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

@Operator1.route('/public/l')
def public():
    return 'For Public Operator'

@Operator1.route('/operator/auth')
@token_required
def auth(**kwargs):
    return 'JWT is verified. Welcome to your Dashboard!'


@Operator1.route('/operator/login', methods=['GET', 'POST'])
def operator_login():
    try:
        username = request.form['username']
        password = request.form['password']
        date = datetime.now().date()
        time = datetime.now().time()
        
        user = all_Operator_creds.query.filter_by(username = username, password = password).first()
        
        if user is not None:
            user_current_date_login_status = all_operators_logged_in_status.query.filter_by(operator_username=username, date=date).first()
            if user_current_date_login_status is not None:
                user_current_date_login_status.last_login_time = time
            operator_login_status = all_operators_logged_in_status(operator_username=user.username, mobile=user.mobile, station_no=user.app_id, login_status=True)
            db.session.add(operator_login_status)
            db.session.commit()
            
            session['logged_in'] = True
            token = handlers.create_tocken(username=username, user_id = user.user_id)
            return jsonify({'Response:': 'Operator login successfull!', 'token:': f'{token}'})
        else:
            return jsonify({'Response:': 'Authentication Failed!'}), 401
    except:
        return jsonify({"Error": "Username or Password Defined"}), 402

@Operator1.route('/operator/logout', methods=['GET', 'POST'])
@token_required
def operator_logout(**kwargs):
    try:
        username = kwargs["token_payload"][1]['username']
        date = datetime.now().date()
        time = datetime.now().time()
        
        user_current_date_login_status = all_operators_logged_in_status.query.filter_by(operator_username=username, date=date).first()
        if user_current_date_login_status is not None:
            user_current_date_login_status.logout_time = time
            user_current_date_login_status.login_status = False
            db.session.commit()
    except:
        return jsonify({'Error': 'Block not executing when Logging out'}), 422




# Check Assigned task By App ID
@Operator1.route('/operator/checkAssignedTaskByAppId/getdata',methods=['GET'])
@token_required
def check_assigned_task_by_app_id(**kwargs):
    try:
        # Extract parameters from the URL
        date = datetime.utcnow().date()
        building_no = request.args.get('building_no')
        floor_no = request.args.get('floor_no')
        line_no = request.args.get('line_no')
        station_no = request.args.get('station_no')
        app_id = request.args.get('app_id')
        
        assigned_task_to_station = gurugram_assigned_task_by_admin.query.filter_by(building_no=building_no, floor_no=floor_no, date=date, station_no = station_no,  line_no = line_no, app_id = app_id).first()
        
        if assigned_task_to_station:
            return jsonify({'Assigned:': 'Task has Assigned to this station', 'operator_username:': f'{assigned_task_to_station.operator_username}'})
        else:
            return jsonify({'Not Assigned:': 'Task Has not Assigned To This Satation Yet'})
    except Exception as e:
        return jsonify({'Error in Try block:': f'{e}'}), 402