from flask import request, session, jsonify, current_app
from collections import Counter
from Database.models import Operator_creds, fpa_and_set_up_approved_records, reading_params, stations, work_assigned_to_operator, processes_info, parameters_info, check_sheet, notify_to_incharge
from Database.init_and_conf import db
from datetime import datetime
from Config.token_handler import TokenRequirements
import pytz

def operator_login(data):
    try:
        employee_id = data.get('employee_code')
        password = data.get('password')
        # date = datetime.now().date()
        # time = datetime.now().time()
        
        user = Operator_creds.query.filter_by(employee_id=employee_id).first()
        
        if user is not None:
            if user.password == password:
                session['logged_in'] = True
                token = TokenRequirements.create_token(employee_id=employee_id, mobile_no = user.mobile, secret_key=current_app.config['SECRET_KEY'])
                return jsonify({'Response': 'Operator login successfull!', 'token': f'{token}', 'employee_id':f'{user.employee_id}', 'fName': f'{user.fName}', 'lName': f'{user.lName}', 'skill':f'{user.skill_level}'}), 200
            else:
                return jsonify({'Response:': 'Authentication Failed!'}), 401
        else:
            return jsonify({'Response:': 'User Not Found!'}), 404
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def get_task(data):
    try:
        station_id = data.get('station_id')
        current_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
        date = datetime.now(pytz.timezone('Asia/Kolkata')).date()
        get_task_data = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
        if  get_task_data:
            if get_task_data.date==date:
                if get_task_data.end_shift_time>=current_time:
                    assigned_process = get_task_data.process_no
                    print(assigned_process)
                    get_process_data = processes_info.query.filter_by(process_no=assigned_process).first()
                    images_urls = get_process_data.images_urls
                    
                    get_parameters = parameters_info.query.filter_by(process_no=assigned_process).all()
                    process_params_info = []
                    for process_param in get_parameters:
                        # parameter_no = process_param.parameter_no
                        one_param_data = {"parameter_no": process_param.parameter_no, "parameter_name": process_param.parameter_name, "process_no": process_param.process_no, "belongs_to_part": process_param.belongs_to_part, "min": process_param.min,"max": process_param.max, "unit": process_param.unit, "FPA_status": process_param.FPA_status, "readings_is_available": process_param.readings_is_available}
                        # parameter_name = process_param.parameter_name
                        # process_no = process_param.process_no
                        # belongs_to_part = process_param.belongs_to_part
                        # min = process_param.min
                        # max = process_param.max
                        # unit = process_param.unit
                        # FPA_status = process_param.FPA_status
                        # readings_is_available = process_param.readings_is_available
                        # if parameter_no not in process_params_info:
                        #     process_params_info[parameter_no] = []
                        # process_params_info[parameter_no].extend(one_param_data)
                        process_params_info.append(one_param_data)
                    
                    check_sheet_entity_datas = db.session.query(check_sheet.csp_id, check_sheet.csp_name, check_sheet.csp_name_hindi, check_sheet.specification, check_sheet.control_method, check_sheet.frequency).all()
                    check_sheet_datas = [{'csp_id': csp_id, 'csp_name': csp_name, 'csp_name_hindi': csp_name_hindi, 'specification': specification, 'control_method': control_method, 'frequency': frequency} for csp_id, csp_name, csp_name_hindi, specification, control_method, frequency in check_sheet_entity_datas]
                    
                    return jsonify({"urls":images_urls, "check_sheet_datas":check_sheet_datas, "total_check_sheet_params": len(check_sheet_datas), "process_params_info":process_params_info}), 200
                else:
                    return jsonify({"Message":"no task assigned to this station at current shift..."}), 404
            else:
                return jsonify({"Message":"no task assigned to this station today..."}), 404
        else:
            return jsonify({"Message":"This station never assigned any task or doesn't exist..."}), 404
    except Exception as e:
        # db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def checksheet_add_logs():
    try:
        csp_id = request.form['csp_id']
        oprtr_employee_id = request.form['oprtr_employee_id']
        flrInchr_employee_id = request.form['flrInchr_employee_id']
        status_datas = request.form['status_datas']
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def add_work(data):
    try:
        operator_employee_id = data.get('operator_employee_id')
        date = datetime.now().date()

        existing_operator_today = fpa_and_set_up_approved_records.query.filter_by(
            operator_employee_id=operator_employee_id, date=date
        ).first()

        if existing_operator_today:
            updated = False  # Flag to check if update is needed

            for shift in ['start_shift_1', 'start_shift_2', 'end_shift_1', 'end_shift_2']:
                parameters_values_key = f"{shift}_parameters_values"
                time_key = f"{shift}_time"

                if data.get(parameters_values_key) and not getattr(existing_operator_today, parameters_values_key):
                    setattr(existing_operator_today, parameters_values_key, data.get(parameters_values_key))
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
                start_shift_1_parameters_values=data.get('start_shift_1_parameters_values', ''),
                start_shift_1_time=datetime.now().time() if data.get('start_shift_1_parameters_values') else None,
                date=date
            )
            db.session.add(new_work)
            db.session.commit()
            return jsonify({"Message": "Your new work record has been added successfully"}), 200

        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def add_reading(data):
    try:
        operator_employee_id = data.get('operator_employee_id')
        parameter_no = data.get('parameter_no')
        # operator_employee_id = data.get['operator_employee_id']
        date = datetime.now().date()

        existing_parameter = reading_params.query.filter_by(
            parameter_no=parameter_no, date=date
        ).first()

        if existing_parameter:
            updated = False  # Flag to check if update is needed

            for no in [1,2,3,4,5]:
                reading_values_key = f"reading_{no}"
                time_key = f"reading_{no}_time"

                if data.get(reading_values_key) and not getattr(existing_parameter, reading_values_key):
                    setattr(existing_parameter, reading_values_key, data.get(reading_values_key))
                    setattr(existing_parameter, time_key, datetime.now().time())
                    updated = True

            if updated:
                db.session.commit()
                return jsonify({"Message": "Your reading updates have been saved successfully"}), 200
            else:
                return jsonify({"Message": "No reading were necessary to update"}), 200
        else:
            new_reading = reading_params(
                operator_employee_id=operator_employee_id,
                parameter_no=parameter_no,
                reading_1=data.get('reading_1', ''),
                reading_1_time=datetime.now().time() if data.get('reading_1') else None,
                date=date
            )
            db.session.add(new_reading)
            db.session.commit()
            return jsonify({"Message": "Your new reading record has been added successfully"}), 200

        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def update_work_status(data):
    try:
        station_id = data.get('station_id')
        get_station_data = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
        if get_station_data:
            get_station_data.passed = data.get('passed') or get_station_data.passed
            get_station_data.filled = data.get('filled') or get_station_data.filled
            get_station_data.failed = data.get('failed') or get_station_data.failed
            
            db.session.commit()
            return jsonify({"Message":"Part has been updated Successfully"}),200
        else:
            return jsonify({"Message":"No part is available"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def notify_to_incharge_func(data):
    try:
        station_id = data.get("station_id")
        csp_id = data.get("csp_id")
        floor_no = data.get("floor_no")
        date_and_time = datetime.now()
        
        add_notification = notify_to_incharge(station_id=station_id, csp_id=csp_id, floor_no=floor_no, created_at=date_and_time)
        db.session.add(add_notification)
        db.session.commit()
        return jsonify({"Message":f"Notification sent to in-charge for Station ID :{station_id}"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422