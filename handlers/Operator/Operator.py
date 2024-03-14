from flask import Blueprint, render_template, request, session, jsonify, make_response
import handlers
from datetime import datetime, timedelta
from functools import wraps
from Database.models import Operator_creds, floor_incharge_creds, all_sites_information, gurugram_assigned_task_by_admin, all_operators_logged_in_status, work_assigned_to_operator, fpa_and_set_up_approved_records
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
        employee_id = request.form['employee_code']
        password = request.form['password']
        # date = datetime.now().date()
        # time = datetime.now().time()
        
        user = Operator_creds.query.filter_by(employee_id=employee_id).first()
        
        if user is not None:
            if user.password == password:
                session['logged_in'] = True
                token = handlers.create_tocken(employee_id=employee_id, mobile_no = user.mobile)
                return jsonify({'Response:': 'Operator login successfull!', 'token:': f'{token}'})
            else:
                return jsonify({'Response:': 'Authentication Failed!'}), 401
        else:
            return jsonify({'Response:': 'User Not Found!'}), 404
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

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
@Operator1.route('/operator/check/task',methods=['GET'])
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
def add_work():
    # try:
    #     operator_employee_id = request.form['operator_employee_id']
    #     date = datetime.now().date()
        
        
    #     exist_operator_today = fpa_and_set_up_approved_records.query.filter_by(operator_employee_id=operator_employee_id, date=date).first()
    #     if exist_operator_today:
    #         # try:
    #         #     start_shift_1_parameters_values = request.form['start_shift_1_parameters_values']
    #         #     if start_shift_1_parameters_values and not exist_operator_today.start_shift_1_parameters_values:
    #         #         start_shift_1_parameters_values.start_shift_1_parameters_values = start_shift_1_parameters_values or start_shift_1_parameters_values.start_shift_1_parameters_values
    #         #         start_shift_1_time = datetime.now().time()
    #         #         exist_operator_today.start_shift_1_time = start_shift_1_time or exist_operator_today.start_shift_1_time
    #         #         db.session.commit()
    #         #         return jsonify({"Message":"Your work for start shift 1 is added Successfully"}),200
    #         #     else:
    #         #         pass
    #         # except:
    #         #     pass
    #         # start_shift_1_time = request.form['start_shift_1_time']
    #         try:
    #             start_shift_2_parameters_values = request.form['start_shift_2_parameters_values']
    #             if start_shift_2_parameters_values and not exist_operator_today.start_shift_2_parameters_values:
    #                 start_shift_2_parameters_values.start_shift_2_parameters_values = start_shift_2_parameters_values or start_shift_2_parameters_values.start_shift_2_parameters_values
    #                 start_shift_2_time = datetime.now().time()
    #                 exist_operator_today.start_shift_2_time = start_shift_2_time or exist_operator_today.start_shift_2_time
    #                 db.session.commit()
    #                 return jsonify({"Message":"Your work for start shift 2 is added Successfully"}),200
    #             else:
    #                 return jsonify({"Message":f"try block 2 {e}"}), 500
    #                 pass
    #         except:
    #             pass
    #         # start_shift_2_time = request.form['start_shift_2_time']
    #         try:
    #             end_shift_1_parameters_values = request.form['end_shift_1_parameters_values']
    #             if end_shift_1_parameters_values and not exist_operator_today.end_shift_1_parameters_values:
    #                 end_shift_1_parameters_values.end_shift_1_parameters_values = end_shift_1_parameters_values or end_shift_1_parameters_values.end_shift_1_parameters_values
    #                 end_shift_1_time = datetime.now().time()
    #                 exist_operator_today.end_shift_1_time = end_shift_1_time or exist_operator_today.end_shift_1_time
    #                 db.session.commit()
    #                 return jsonify({"Message":"Your work for end shift 1 is added Successfully"}),200
    #             else:
    #                 return jsonify({"Message":f"try block 3 {e}"}), 500
    #                 pass
    #         except:
    #             pass
    #         # end_shift_1_time = request.form['end_shift_1_time']
    #         try:
    #             end_shift_2_parameters_values = request.form['end_shift_2_parameters_values']
    #             if end_shift_2_parameters_values and not exist_operator_today.end_shift_2_parameters_values:
    #                 end_shift_2_parameters_values.end_shift_2_parameters_values = end_shift_2_parameters_values or end_shift_2_parameters_values.end_shift_2_parameters_values
    #                 end_shift_2_time = datetime.now().time()
    #                 exist_operator_today.end_shift_2_time = end_shift_2_time or exist_operator_today.end_shift_2_time
    #                 db.session.commit()
    #                 return jsonify({"Message":"Your work for end shift 2 is added Successfully"}),200
    #             else:
    #                 pass
    #         except Exception as e:
    #             return jsonify({"Message":f"try block 4 {e}"}), 500
    #             pass
    #         # end_shift_2_time = request.form['end_shift_2_time']
    #     else:
    #         try:
    #             start_shift_1_parameters_values = request.form['start_shift_1_parameters_values']
    #             start_shift_1_time = datetime.now().time()
    #             # date = datetime.now().date()
    #             add_new_work = fpa_and_set_up_approved_records(operator_employee_id=operator_employee_id, start_shift_1_parameters_values=start_shift_1_parameters_values, start_shift_1_time=start_shift_1_time, date=date)
    #             db.session.add(add_new_work)
    #             db.session.commit()
    #             return jsonify({"Message":"Your work for start shift 1 is added Successfully"}),200
    #         except:
    #             return jsonify({"Message":f"try block 1 {e}"}), 500
    #             pass
    
    
    try:
        operator_employee_id = request.form['operator_employee_id']
        date = datetime.now().date()

        existing_operator_today = fpa_and_set_up_approved_records.query.filter_by(
            operator_employee_id=operator_employee_id, date=date
        ).first()

        if existing_operator_today:
            updated = False  # Flag to check if update is needed

            for shift in ['start_shift_1', 'start_shift_2', 'end_shift_1', 'end_shift_2']:
                parameters_values_key = f"{shift}_parameters_values"
                time_key = f"{shift}_time"

                if request.form.get(parameters_values_key) and not getattr(existing_operator_today, parameters_values_key):
                    setattr(existing_operator_today, parameters_values_key, request.form[parameters_values_key])
                    setattr(existing_operator_today, time_key, datetime.now().time())
                    updated = True

            if updated:
                db.session.commit()
                return jsonify({"Message": "Your work updates have been saved successfully"}), 200
            else:
                return jsonify({"Message": "No updates were necessary"}), 200
        else:
            new_work = fpa_and_set_up_approved_records(
                operator_employee_id=operator_employee_id,
                start_shift_1_parameters_values=request.form.get('start_shift_1_parameters_values', ''),
                start_shift_1_time=datetime.now().time() if request.form.get('start_shift_1_parameters_values') else None,
                date=date
            )
            db.session.add(new_work)
            db.session.commit()
            return jsonify({"Message": "Your new work record has been added successfully"}), 200

        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422