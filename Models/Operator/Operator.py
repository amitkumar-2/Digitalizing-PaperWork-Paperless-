from flask import request, session, jsonify, current_app
from collections import Counter
from Database.models import Operator_creds, fpa_and_set_up_approved_records, reading_params, stations, work_assigned_to_operator
from Database.init_and_conf import db
from datetime import datetime
from Config.token_handler import TokenRequirements

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
                return jsonify({'Response': 'Operator login successfull!', 'token': f'{token}', 'station_id':f'{user.employee_id}', 'fName': f'{user.fName}', 'lName': f'{user.lName}', 'skill':f'{user.skill_level}'}), 200
            else:
                return jsonify({'Response:': 'Authentication Failed!'}), 401
        else:
            return jsonify({'Response:': 'User Not Found!'}), 404
    except Exception as e:
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


def stations_info(data):
    try:
        floor_no = data.get('floor_no')
        all_stations = []

        current_lines_data = stations.query.filter_by(floor_no=floor_no).all()
        if current_lines_data:
            for entity in range(0, len(current_lines_data)):
                all_stations.append(current_lines_data[entity].line_no)
            # all_duplicates = dict(Counter(all_stations))
            
            # Create a dictionary to store the results
            stations_dict = {}

            # Iterate over the list to populate the dictionary
            for station in all_stations:
                # Extract the prefix (assuming the prefix always ends before the last ' S')
                prefix = station.rsplit(' S', 1)[0]
                # Add the station to the list associated with the prefix in the dictionary
                if prefix in stations_dict:
                    stations_dict[prefix].append(station)
                else:
                    stations_dict[prefix] = [station]
                    
            return jsonify({"totalLines":f"{len(stations_dict)}", "lines":f'{list(stations_dict)}', "All_stations":f'{stations_dict}'})
        else:
            return "Error"
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def stations_current_status(data):
    try:
        all_stations_status = db.session.query(work_assigned_to_operator.station_id, work_assigned_to_operator.employee_id, work_assigned_to_operator.part_no, work_assigned_to_operator.process_no, work_assigned_to_operator.start_shift_time, work_assigned_to_operator.end_shift_time,work_assigned_to_operator.assigned_by_owner, work_assigned_to_operator.total_assigned_task, work_assigned_to_operator.failed, work_assigned_to_operator.passed, work_assigned_to_operator.filled, work_assigned_to_operator.shift).all()
        all_stations_data = [{'station_id': station_id, 'employee_id': employee_id, 'part_no': part_no, 'process_no': process_no, 'start_shift_time': str(start_shift_time), 'end_shift_time': str(end_shift_time), 'assigned_by_owner': assigned_by_owner, 'total_assigned_task': total_assigned_task, 'failed': failed, 'passed': passed, 'filled': filled, 'shift': shift} for station_id, employee_id, part_no, process_no, start_shift_time, end_shift_time, assigned_by_owner, total_assigned_task, failed, passed, filled, shift in all_stations_status]
        # print(all_stations_data)
        return jsonify({"all_stattions_data: ": all_stations_data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422