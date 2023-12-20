from flask import Blueprint, render_template, request, session, jsonify, make_response
import handlers
from datetime import datetime, timedelta
from functools import wraps
from Database.models import Operator_creds, floor_incharge, sites_information, assigned_task_by_admin
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
            
            if payload == False:
                # Call the original function with the token payload
                return func(*args, **kwargs)
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


@Operator1.route('/operator/login', methods=['GET'])
def operator_login():
    try:
        username = request.form['username']
        password = request.form['password']
        
        user = Operator_creds.query.filter_by(username = username, password = password).first()
        if user is not None:
            session['logged_in'] = True
            token = handlers.create_tocken(username=username, user_id = user.user_id)
            return jsonify({'Response:': 'Operator login successfull!', 'token:': f'{token}'})
        else:
            return jsonify({'Response:': 'Authentication Failed!'})
    except:
        return jsonify({"Error": "Username or Password Defined"})




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
        
        assigned_task_to_station = assigned_task_by_admin.query.filter_by(building_no=building_no, floor_no=floor_no, date=date, station_no = station_no,  line_no = line_no, app_id = app_id).first()
        
        if assigned_task_to_station:
            return jsonify({'Assigned:': 'Task has Assigned to this station', 'operator_username:': f'{assigned_task_to_station.operator_username}'})
        else:
            return jsonify({'Not Assigned:': 'Task Has not Assigned To This Satation Yet'})
    except Exception as e:
        return jsonify({'Error in Try block:': f'{e}'})