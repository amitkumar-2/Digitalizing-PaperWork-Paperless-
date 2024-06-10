from flask import Blueprint, render_template, request, session, jsonify, make_response, current_app
# from handlers import is_token_expired
from Config.token_handler import TokenRequirements
from datetime import datetime, timedelta
from functools import wraps
from Database.models import Operator_creds, floor_incharge_creds, work_assigned_to_operator, fpa_and_set_up_approved_records, reading_params
from Database.init_and_conf import db
from Models.Operator.Operator import operator_login, add_fpa_data, add_reading, get_task, notify_to_incharge_func, check_fpa_status, update_work_status, add_checksheet_data, get_reasons_for_items, add_failed_items, get_update_on_csp


Operator1=Blueprint('Operator', __name__)



# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token')
#         if not token:
#             return jsonify({'Alert!': 'Token is missing!'})
#         try:
#             payload = is_token_expired(token)
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

@Operator1.route('/public/l')
def public():
    return 'For Public Operator'

@Operator1.route('/operator/auth')
@TokenRequirements.token_required
def auth(**kwargs):
    return 'JWT is verified. Welcome to your Dashboard!'


@Operator1.route('/operator/login', methods=['POST'])
def operator_login_handler():
    return operator_login(request.form)

@Operator1.route('/operator/logout', methods=['POST'])
@TokenRequirements.token_required
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

@Operator1.route('/operator/get_task', methods=['POST'])
@TokenRequirements.token_required
def get_task_handler(**kwargs):
    return get_task(request.form)


# Check Assigned task By App ID
@Operator1.route('/operator/check/task',methods=['POST'])
# @token_required
def check_assigned_task_by_app_id(**kwargs):
    try:
        # Extract parameters from the URL
        date = datetime.utcnow().date()
        station_id = request.args.get('station_id')
        print(station_id)
        
        assigned_task_to_station = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
        
        if assigned_task_to_station:
            return jsonify({'Assigned:': 'Task has Assigned to this station'})
        else:
            return jsonify({'Not Assigned:': 'Task Has not Assigned To This Satation Yet'})
    except Exception as e:
        return jsonify({'Error in Try block:': f'{e}'}), 402





#########################################################################################################################
################################################# update assigned task datas ############################################
#########################################################################################################################

@Operator1.route("/operator/add_and_update/work", methods=['POST'])
# @token_required
def update_work_status_handler():
    return update_work_status(request.form)


##################################################### add and update readings by operator ##########################################
@Operator1.route("/operator/add_and_update/readings", methods=['POST'])
# @token_required
def add_reading_handler():
    return add_reading(request.form)


@Operator1.route("/operator/notify", methods=["POST"])
@TokenRequirements.token_required
def notify_to_incharge_func_handler(**kwargs):
    return notify_to_incharge_func(request.form)

@Operator1.route("/operator/get_csp_status", methods=["POST"])
@TokenRequirements.token_required
def get_update_on_csp_handler(**kwargs):
    return get_update_on_csp(request.form)


@Operator1.route("/operator/add_fpa_data", methods=["POST"])
@TokenRequirements.token_required
def add_fpa_data_handler(**kwargs):
    return add_fpa_data(request.form)


@Operator1.route("/operator/check_fpa_status", methods=["POST"])
@TokenRequirements.token_required
def check_fpa_status_handler(**kwargs):
    return check_fpa_status(request.form)


@Operator1.route("/operator/add_checksheet_data", methods=["POST"])
@TokenRequirements.token_required
def add_checksheet_data_handler(**kwargs):
    return add_checksheet_data(request.form)

################################### Get the reasons for the item data ##########################################
@Operator1.route("/operator/get_reasons_for_items", methods=['POST'])
@TokenRequirements.token_required
def get_reasons_for_items_handler(**kwargs):
    return get_reasons_for_items(request.form)

################################### add failed items with reason ##########################################
@Operator1.route("/operator/add_failed_items", methods=['POST'])
@TokenRequirements.token_required
def add_failed_items_handler(**kwargs):
    return add_failed_items(request.form)