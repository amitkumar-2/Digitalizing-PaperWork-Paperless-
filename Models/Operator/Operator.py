from flask import request, session, jsonify, current_app
from collections import Counter
from Database.models import Operator_creds, fpa_and_set_up_approved_records, reading_params, stations, work_assigned_to_operator, processes_info, parameters_info, check_sheet, notify_to_incharge, check_sheet_data, reasons, failed_items
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
                return jsonify({'Response': 'Operator login successfull!', 'token': f'{token}', 'employee_id':f'{user.employee_id}', 'fName': f'{user.fName}', 'lName': f'{user.lName}', 'skill':f'{user.skill_level}', 'password':f'{user.password}', 'mobile':f'{user.mobile}', 'email':f'{user.email}', 'dob':f'{user.dob}'}), 200
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
                    task_data = {
                        # 'station_id': get_task_data.station_id,
                        'part_no': get_task_data.part_no,
                        'process_no':get_task_data.process_no,
                        'start_shift_time':get_task_data.start_shift_time.strftime('%H:%M:%S'),
                        'end_shift_time':get_task_data.end_shift_time.strftime('%H:%M:%S'),
                        # 'assigned_by_owner':get_task_data.assigned_by_owner,
                        # 'operator_login_status':get_task_data.operator_login_status,
                        'flrInchr_employee_id':get_task_data.assigned_by_owner,
                        'shift':get_task_data.shift,
                        'total_assigned_task':get_task_data.total_assigned_task,
                        # 'left_for_rework':get_task_data.left_for_rework,
                        'passed':get_task_data.passed,
                        'filled':get_task_data.filled,
                        'failed':get_task_data.failed,
                        'temp_task_id': get_task_data.task_id,
                        'station_precidency': get_task_data.station_precedency
                        # Add other relevant fields here
                    }
                    
                    assigned_process = get_task_data.process_no
                    print(assigned_process)
                    get_process_data = processes_info.query.filter_by(process_no=assigned_process).first()
                    try:
                        images_urls = get_process_data.images_urls
                    except:
                        images_urls = "Images not availabel for this process"
                    
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
                    
                    check_sheet_status_for_operator = check_sheet_data.query.filter_by(station_id=station_id).first()
                    if check_sheet_status_for_operator:
                        check_sheet_fill_status = True
                    else:
                        check_sheet_fill_status = False
                    
                    get_readings_data = reading_params.query.filter_by(station_id=station_id, date=date).first()
                    if get_readings_data:
                        station_reading_data = {'reading_1': get_readings_data.reading_1, 'reading_2': get_readings_data.reading_2, 'reading_3': get_readings_data.reading_3, 'reading_4': get_readings_data.reading_4, 'reading_5': get_readings_data.reading_5}
                    else:
                        station_reading_data = {'reading_1': "null", 'reading_2': "null", 'reading_3': "null", 'reading_4': "null", 'reading_5': "null"}
                    
                    get_fpa_status = fpa_and_set_up_approved_records.query.filter_by(station_id=station_id).first()
                    station_fpa_data = []
                    if get_fpa_status:
                        station_fpa_data.append({"station_id": get_fpa_status.station_id, "start_shift_1_parameters_values": get_fpa_status.start_shift_1_parameters_values, "start_shift_2_parameters_values": get_fpa_status.start_shift_2_parameters_values, "end_shift_1_parameters_values": get_fpa_status.end_shift_1_parameters_values, "end_shift_2_parameters_values": get_fpa_status.end_shift_2_parameters_values})
                    else:
                        station_fpa_data = None
                    
                    return jsonify({"work_operator_data":task_data, "urls":images_urls, "check_sheet_datas":check_sheet_datas, "total_check_sheet_params": len(check_sheet_datas), "process_params_info":process_params_info, "check_sheet_fill_status":check_sheet_fill_status, "station_reading_data": station_reading_data, "station_fpa_data": station_fpa_data}), 200
                else:
                    return jsonify({"Message":"no task assigned to this station at current shift..."}), 404
            else:
                return jsonify({"Message":"no task assigned to this station today..."}), 404
        else:
            return jsonify({"Message":"This station never assigned any task or doesn't exist..."}), 404
    except Exception as e:
        # db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def checksheet_add_logs(data):
    try:
        csp_id = data.get('csp_id')
        oprtr_employee_id = data.get('oprtr_employee_id')
        flrInchr_employee_id = data.get('flrInchr_employee_id')
        status_datas = data.get('status_datas')
        
        add_checksheet_data = check_sheet_data(csp_id=csp_id, oprtr_employee_id=oprtr_employee_id, flrInchr_employee_id=flrInchr_employee_id, status_datas=status_datas)
        db.session.add(add_checksheet_data)
        db.session.commit()
        return jsonify({"Message": "Check sheet data submited successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def add_checksheet_data(data):
    try:
        station_id = data.get('station_id')
        oprtr_employee_id = data.get('oprtr_employee_id')
        flrInchr_employee_id = data.get('flrInchr_employee_id')
        status_datas = data.get('status_datas')
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        
        add_checksheet_data = check_sheet_data(oprtr_employee_id=oprtr_employee_id, flrInchr_employee_id=flrInchr_employee_id, status_datas=status_datas, station_id=station_id, date=current_date, time=current_time)
        db.session.add(add_checksheet_data)
        db.session.commit()
        return jsonify({"Message": "Check sheet data submited successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def add_fpa_data(data):
    try:
        station_id = data.get('station_id')
        date = datetime.now().date()
        

        existing_operator_today = fpa_and_set_up_approved_records.query.filter_by(
            station_id=station_id, date=date
        ).first()
        running_task_station_id = work_assigned_to_operator.query.filter_by(station_id=station_id).first()

        if existing_operator_today:
            # if len(existing_operator_today.end_shift_2_time) > 4:
            #     return jsonify({"Message": "You have already submitted the end shift 2 value."}), 301
            # elif len(existing_operator_today.end_shift_1_time) > 4:
            #     return jsonify({"Message": "You have already submitted the end shift 1 value."}), 301
            # elif len(existing_operator_today.start_shift_2_time) > 4:
            #     return jsonify({"Message": "You have already submitted the start shift 2 value."}), 301
            # elif len(existing_operator_today.start_shift_1_time) > 4:
            #     return jsonify({"Message": "You have already submitted the start shift 1 value."}), 301
            updated = False  # Flag to check if update is needed

            for shift in ['start_shift_1', 'start_shift_2', 'end_shift_1', 'end_shift_2']:
                parameters_values_key = f"{shift}_parameters_values"
                time_key = f"{shift}_time"

                if data.get(parameters_values_key) and not getattr(existing_operator_today, parameters_values_key):
                    setattr(existing_operator_today, parameters_values_key, data.get(parameters_values_key))
                    setattr(existing_operator_today, time_key, datetime.now().time())
                    
                    running_task_station_id.passed = data.get('passed') or running_task_station_id.passed
                    running_task_station_id.failed = data.get('failed') or running_task_station_id.failed
                    
                    updated = True

            if updated:
                # db.session.add(running_task_station_id)
                db.session.commit()
                return jsonify({"Message": "Your work updates have been saved successfully"}), 201
            else:
                return jsonify({"Message": f"No updates were necessary for this station"}), 200
        else:
            new_work = fpa_and_set_up_approved_records(
                station_id=station_id,
                start_shift_1_parameters_values=data.get('start_shift_1_parameters_values', ''),
                start_shift_1_time=datetime.now().time() if data.get('start_shift_1_parameters_values') else None,
                date=date
            )
            running_task_station_id.passed = data.get('passed') or running_task_station_id.passed
            running_task_station_id.failed = data.get('failed') or running_task_station_id.failed
            
            db.session.add(new_work)
            db.session.commit()
            return jsonify({"Message": "Your new work record has been added successfully"}), 200

        
    except Exception as e:
        db.session.rollback()
        print("###########", f'Block is not able to execute successfully {e}')
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def check_fpa_status(data):
    try:
        precedency_no = int(data.get('precedency_no'))
        if precedency_no == 1:
            precedency_no = -1
        else:
            precedency_no = (int(data.get('precedency_no')) - 1)
        part_no = data.get('part_no')
        temp_task_id = data.get('temp_task_id')
        fpa_check_count = int(data.get('fpa_check_count'))
        if (fpa_check_count == 2 or fpa_check_count == 1) and precedency_no == -1:
            precedency_no = 0
        
        if fpa_check_count == 2:
            precedency_no = 0
        
        previous_station_fpa_data = {}
        
        get_part_stations = work_assigned_to_operator.query.filter_by(part_no=part_no, task_id=temp_task_id).all()
        if get_part_stations:
            for station in get_part_stations:
                if precedency_no == 0:
                    for station in get_part_stations:
                        if precedency_no < station.station_precedency:
                            precedency_no = station.station_precedency
                if station.station_precedency == precedency_no:
                    before_station_fpa_status = fpa_and_set_up_approved_records.query.filter_by(station_id=station.station_id).first()
                    if before_station_fpa_status:
                        start_shift_1_parameters_values = None
                        start_shift_2_parameters_values = None
                        end_shift_1_parameters_values = None
                        end_shift_2_parameters_values = None
                        
                        if before_station_fpa_status.start_shift_1_time:
                            start_shift_1_parameters_values = True
                            print(start_shift_1_parameters_values)
                        if before_station_fpa_status.start_shift_2_time:
                            start_shift_2_parameters_values = True
                        if before_station_fpa_status.end_shift_1_time:
                            end_shift_1_parameters_values = True
                        if before_station_fpa_status.end_shift_2_time:
                            end_shift_2_parameters_values = True
                        previous_station_fpa_data["station_id"] = before_station_fpa_status.station_id
                        previous_station_fpa_data["start_shift_1_parameters_values"] = start_shift_1_parameters_values or before_station_fpa_status.start_shift_1_parameters_values
                        previous_station_fpa_data["start_shift_2_parameters_values"] = start_shift_2_parameters_values or before_station_fpa_status.start_shift_2_parameters_values
                        previous_station_fpa_data["end_shift_1_parameters_values"] = end_shift_1_parameters_values or before_station_fpa_status.end_shift_1_parameters_values
                        previous_station_fpa_data["end_shift_2_parameters_values"] = end_shift_2_parameters_values or before_station_fpa_status.end_shift_2_parameters_values
                        return jsonify({"before_station_fpa_status": previous_station_fpa_data}), 200
                    else:
                        return jsonify({"before_station_fpa_status": f"data not found for station {station.station_id}"}), 444 # Custom status code
                else:
                    continue
                    # return jsonify({"Message": "This is the fpa test for the first station"}), 210 # custom status code
            return jsonify({"Message": "This is the fpa test for the first station"}), 210 # custom status code
        else:
            return jsonify({"Message": "Any how task is not assign for this part or task id is not exist."}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def add_reading(data):
    try:
        station_id = data.get('station_id')
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
                station_id=station_id,
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

def add_failed_items(data):
    try:
        station_id = data.get('station_id')
        item_id = data.get('item_id')
        part_no = data.get('part_no')
        reason_id = data.get('reason_id')
        remark = data.get('remark')
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        get_station_data = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
        if get_station_data:
            get_station_data.passed = data.get('passed') or get_station_data.passed
            get_station_data.filled = data.get('filled') or get_station_data.filled
            get_station_data.failed = data.get('failed') or get_station_data.failed
            
            add_failed_item = failed_items(item_id=item_id, part_no=part_no, reason_id=reason_id, station_id=station_id, time=current_time, date=current_date, remarks=remark)

            db.session.add(add_failed_item)
            db.session.commit()
            return jsonify({"Message":"Part has been updated Successfully"}),200
        else:
            return jsonify({"Message":"No task assigned to this station"}), 404
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
        date = datetime.now().date()
        time = datetime.now().time()
        
        add_notification = notify_to_incharge(station_id=station_id, csp_id=csp_id, floor_no=floor_no, created_date=date, created_time=time)
        db.session.add(add_notification)
        db.session.commit()
        # Retrieve the primary key
        notification_id = add_notification.notification_id
        return jsonify({"Message":f"Notification sent to in-charge for Station ID :{station_id}", "Notification_id": f"{notification_id}"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def get_update_on_csp(data):
    try:
        notification_id = data.get("notification_id")
        notification = notify_to_incharge.query.filter_by(notification_id=notification_id).first()
        if notification:
            approved_status = notification.approved_status
            return jsonify({"Approved status": f"{approved_status}"}), 200
        return jsonify({"Message": "This notification has been deleted or not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

# def check_fpa_status(data):
#     try:
#         station_id = data.get("station_id")
#         part_no = data.get("part_no")
#         shift = data.get("shift")
#         # date_and_time = datetime.now()
        
#         add_notification = fpa_and_set_up_approved_records.query.filter_by(station_id=station_id, part_no=part_no, shift=shift).first()
#         db.session.add(add_notification)
#         db.session.commit()
#         return jsonify({"Message":f"Notification sent to in-charge for Station ID :{station_id}"}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422



# def check_fpa_status(data):
#     try:
#         station_id=data.get('station_id')
#         # Fetch all station_ids for the given floor_no
#         is_not_approved = False
#         station_data = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
#         if station_data:
#             if (station_data.check_fpa_status_at + 2) < station_data.passed:
#                 station_data.check_fpa_status_at = station_data.passed
#                 db.session.commit()
#             else:
#                 pass
            
#             fpa_status_data = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
#             if (fpa_status_data.check_fpa_status_at+2) <= fpa_status_data.passed:
#                 is_not_approved = True
#             elif (fpa_status_data.check_fpa_status_at+2) >= fpa_status_data.passed:
#                 fpa_status_data.passed = data.get('passed') or fpa_status_data.passed
#                 fpa_status_data.failed = data.get('failed') or fpa_status_data.failed
                
#                 db.session.commit()
#                 return jsonify({"Message": "FPA Status updated Successfully"}), 201
#             # else:
#             #     return jsonify({"Message":"Part has been updated Successfully"}),200
            
#             return jsonify({" For this station_id is_approved value is":is_not_approved}),200
#         else:
#             return jsonify({"Message": "No stations found for the station_id."}), 404
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'Error': f'Failed to fetch data: {e}'}), 500


def get_reasons_for_items(data):
    try:
        process_no=data.get('process_no')
        if process_no:
            exist_reasons= reasons.query.filter_by(process_no=process_no).all()
            if exist_reasons:
                reasons_data = [
                {'reason_id': reasons.reason_id, 'reason': reasons.reason}
                        for reasons in exist_reasons]
                return jsonify({"reasons": reasons_data}), 200
            else:
                return jsonify({"Message": "No reasons found for the floor_no."}), 404
        else:
            return jsonify({"Message": "Please provide floor_no."}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Failed to fetch data: {e}'}), 500

