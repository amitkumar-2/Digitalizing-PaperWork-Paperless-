from flask import request, jsonify, session, current_app
import pytz
from Database.init_and_conf import db
from Database.models import floor_incharge_creds, Operator_creds, parts_info, processes_info, parameters_info, check_sheet_data, stations, work_assigned_to_operator, work_assigned_to_operator_logs, check_sheet, notify_to_incharge
# from handlers import create_tocken
from Config.token_handler import TokenRequirements
from datetime import datetime, timedelta
from Services.AWS_S3 import return_s3_client
from Config.creds import BaseConfig
# from os import path

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


def login(data):
    try:
        employee_id = data.get('employee_id')
        password = data.get('password')
        
        user = floor_incharge_creds.query.filter_by(employee_id=employee_id).first()
        if user is not None:
            if user.password == password:
                session['logged_in'] = True
                token = TokenRequirements.create_token(employee_id=user.employee_id, mobile_no=user.mobile, secret_key=current_app.config['SECRET_KEY'])
                return jsonify({'Response:': 'Floor_Incharge login successfull!', 'token': f'{token}', 'employee_id':f'{user.employee_id}', 'fName':f'{user.fName}', 'lName':f'{user.lName}', 'building_no': f'{user.building_no}', 'floor_no': f'{user.floor_no}'}), 200
            else:
                return jsonify({'Response:': 'Authentication Failed!'}), 401
        else:
            return jsonify({'Response:': 'User Not Found!'}), 404
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def operator_signup(data):
    try:
        employee_id = data.get('employee_id')
        fName = data.get('fName')
        try:
            mName = data.get('mName')
        except:
            mName = ''
        try:
            lName = data.get('lName')
        except:
            lName = ''
        skill_level = data.get('skill_level')
        dob = data.get('dob')
        mobile = data.get('mobile')
        email =data.get('email')
        password = data.get('password')
        
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

def add_part(data):
    try:
        part_name = data.get('part_name')
        if len(part_name) <= 0:
            return  jsonify({"error":"Part name cannot be empty"}),406
        part_no = data.get('part_id')
        if len(part_no) <= 0:
            return  jsonify({"error":"Part no cannot be empty"}),406
        added_by_owner = data.get('added_by_owner')

        exist_part_no = parts_info.query.filter_by(part_no=part_no).first()
        if exist_part_no:
            return jsonify({"Message": "This Part Number already exists."}), 200
        else:
            new_parts = parts_info(part_name=part_name, part_no=part_no, added_by_owner=added_by_owner)
            db.session.add(new_parts)
            db.session.commit()
            return jsonify({"Message": "New Part has been added Successfully.", "ParName": f"{part_name}"}),  201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def get_parts():
    """Returns list of available parts"""
    try:
        data=db.session.query(parts_info.part_no, parts_info.part_name).all()
        # print(len(data))
        # for i in range(len(data)):
        #     part_name = data[i].part_name
        #     part_no = data[i].part_no
        parts_data = [{'part_name': part_name, 'part_no': part_no} for part_no, part_name in data]
        return jsonify({"data": parts_data}), 200
    except Exception as e:
        return jsonify({'Error': f'Block is not able to fetch records {e}'}), 500

def update_part(data):
    try:
        part_no = data.get('part_no')
        get_part = parts_info.query.filter_by(part_no=part_no).first()
        if get_part:
            get_part.part_name = data.get('parn_name') or get_part.part_name
            get_part.part_no = data.get('part_no') or get_part.part_no
            get_part.added_by_owner = data.get('added_by_owner') or get_part.added_by_owner
            
            db.session.commit()
            return jsonify({"Message":"Part has been updated Successfully"}),200
        else:
            return jsonify({"Message":"No part is available"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to fetch records {e}'}), 500

def disable_part(data):
    try:
        part_no=data.get('part_no')
        disabled = data.get('disabled')
        get_part = parts_info.query.filter_by(part_no=part_no).first()
        if get_part:
            if get_part.disabled==1:
                return jsonify({"Message": "Part is already disabled"}), 200

            if disabled == "true" or disabled == "1":
                get_part.disabled = True
                db.session.commit()
                return jsonify({"Message":"Part has been Disabled Successfully"}),200
            else:
                return jsonify({"Message": "Invalid value for 'disabled' parameter"}), 400
        else:
            return jsonify({"Message": "Part not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def add_process(data, files):
    try:
        process_name = data.get('process_name')
        if len(process_name) <= 0:
            return  jsonify({"error":"Part name cannot be empty"}),406
        process_no = data.get('process_id')
        if len(process_no) <= 0:
            return  jsonify({"error":"Part name cannot be empty"}),406
        belongs_to_part = data.get('belongs_to_part')
        if len(belongs_to_part) <= 0:
            return  jsonify({"error":"Part name cannot be empty"}),406
        added_by_owner = data.get('added_by_owner')
        if len(added_by_owner) <= 0:
            return  jsonify({"error":"Part name cannot be empty"}),406
        files = files.getlist('file')
        
        # s3_client = return_s3_client()
        

        exist_part_no = parts_info.query.filter_by(part_no=belongs_to_part).first()
        if exist_part_no:
            exist_process_no = processes_info.query.filter_by(process_no=process_no).first()
            if exist_process_no:
                return jsonify({"Message": "This Process number already exists."})
            
            else:
                # files_urls = []
                # if files:
                #     for file in files:
                #         file_path = f"{belongs_to_part}/{file.filename}"
                #         print(file_path)
                #         s3_client.upload_fileobj(
                #             file,
                #             BaseConfig.AWS_S3_BUCKET,
                #             file_path)

                #         files_urls.append(f'https://{BaseConfig.AWS_S3_BUCKET}.s3.{BaseConfig.AWS_S3_REGION}.amazonaws.com/{file_path}')
                #         urls_str = ', '.join(files_urls)
                #         # print(urls_str)
                    
                # else:
                #     files_urls = None
                
                # new_process = processes_info(process_name=process_name, process_no=process_no, belongs_to_part=belongs_to_part, images_urls=urls_str, added_by_owner=added_by_owner)
                new_process = processes_info(process_name=process_name, process_no=process_no, belongs_to_part=belongs_to_part, added_by_owner=added_by_owner)
                db.session.add(new_process)
                db.session.commit()
                return jsonify({"Message": "New Process has been added Successfully.", "ProcessName": f"{process_name}"}),  201
        else:
            return jsonify({"Message":"Part does not exist."}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def get_processes(data):
    """Returns list of available parts"""
    try:
        part_no = data.get('part_no')
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
                return jsonify({"data": process_data}), 200
            else:
                return jsonify({'Message': 'No processes available for this part'}), 404
        else:
            return jsonify( {'Message':'No such Part Found.'} ), 404
    except Exception as e:
        return jsonify({'Error': f'Block is not able to fetch records {e}'}), 500

def update_processes(data):
    try:
        process_name = data.get('process_name')
        process_no = data.get('process_no')
        belongs_to_part = data.get('belongs_to_part')
        added_by_owner = data.get('added_by_owner')
        files = files.getlist('file')
        
        s3_client = return_s3_client()
        

        exist_part_no = parts_info.query.filter_by(part_no=belongs_to_part).first()
        if exist_part_no:
            exist_process_no = processes_info.query.filter_by(process_no=process_no).first()
            if exist_process_no:
                # return jsonify({"Message": "This Process number already exists."})
                files_urls = []
                if files:
                    for file in files:
                        file_path = f"{belongs_to_part}/{file.filename}"
                        print(file_path)
                        s3_client.upload_fileobj(
                            file,
                            BaseConfig.AWS_S3_BUCKET,
                            file_path)

                        files_urls.append(f'https://{BaseConfig.AWS_S3_BUCKET}.s3.{BaseConfig.AWS_S3_REGION}.amazonaws.com/{file_path}')
                        urls_str = ', '.join(files_urls)
                        # print(urls_str)
                    
                else:
                    files_urls = None
                
                exist_process_no.process_name = process_name
                exist_process_no.belongs_to_part = belongs_to_part
                exist_process_no.added_by_owner = added_by_owner
                exist_process_no.images_urls = urls_str
                db.session.commit()
                return jsonify({"Message": "Process has been updated Successfully.", "ProcessName": f"{process_name}"}),  200
            
            else:
                return jsonify({"Message": "Process does not exist."}), 404
        else:
            return jsonify({"Message":"Part does not exist."}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to fetch records {e}'}), 422


def add_parameter(data):
    try:
        parameter_name = data.get('parameter_name')
        parameter_no = data.get('parameter_no')
        process_no = data.get('process_no')
        belongs_to_part = data.get('belongs_to_part')
        added_by_owner = data.get('added_by_owner')
        min = data.get('min')
        max = data.get('max')
        unit = data.get('unit')
        
        FPA_status = data.get('FPA_status')
        FPA_status = bool(FPA_status)
        
        readings_is_available = data.get('readings_is_available')
        readings_is_available = bool(readings_is_available)
        
        exist_process_no = processes_info.query.filter_by(process_no=process_no).first()
        
        if exist_process_no:        
            exist_parameter_no =   parameters_info.query.filter_by(parameter_no=parameter_no).first()
            if exist_parameter_no:
                return jsonify({"Message": "This Parameters number already exists."}), 200
            
            else:
                new_process = parameters_info(parameter_name=parameter_name, parameter_no=parameter_no, process_no=process_no, belongs_to_part=belongs_to_part, min=min, max=max, unit=unit, FPA_status=FPA_status, added_by_owner=added_by_owner)
                db.session.add(new_process)
                db.session.commit()
                return jsonify({"Message": "New Process has been added Successfully.", "ProcessName": f"{parameter_name}"}),  201
        else:
            return jsonify({"Message":"Process does not exist."}), 404
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def get_parameter(data):
    """Returns list of available parameters for process"""
    try:
        part_no = data.get('part_no')
        process_no=data.get('process_no')
        exist_part = parts_info.query.filter_by(part_no=part_no).first()
        if exist_part:
            exist_processes = processes_info.query.filter_by(process_no=process_no).first()
            if exist_processes:
                exist_parameters=parameters_info.query.filter_by(process_no=process_no).all()
                if exist_parameters:
                    print(exist_parameters[0].parameter_name)
                    parameters_data = [
                        {'parameter_name': parameters.parameter_name, 'parameter_no': parameters.parameter_no, 'min':parameters.min, 'max':parameters.max, 'unit':parameters.unit, 'FPA_status':parameters.FPA_status, 'readings_is_available':parameters.readings_is_available}
                        for parameters in exist_parameters]
                # print(process_data)
                    return jsonify({"data: ": parameters_data}), 200
                else:
                    return jsonify({'Message': 'No parameters  available for this part and process'}), 404
            else:
                return jsonify({'Message': 'No processs  available for this part'}), 404
        else:
            return jsonify( {'Message':'No such Part Found.'} ), 404
    except Exception as e:
        return jsonify({'Error': f'Block is not able to fetch records {e}'}), 422

def update_parameter(data):
    try:
        parameter_no = data.get('parameter_no')
        parameter_name = data.get('parameter_name')
        min = data.get('min')
        max = data.get('max')
        unit= data.get('unit')
        FPA_status = data.get('FPA_status')
        readings_is_available = data.get('readings_is_available')
        exist_parameter=parameters_info.query.filter_by(parameter_no=parameter_no).one()
        if exist_parameter:
            exist_parameter.parameter_name = parameter_name
            exist_parameter.min = min
            exist_parameter.max = max
            exist_parameter.unit = unit
            exist_parameter.FPA_status = FPA_status
            exist_parameter.readings_is_available = readings_is_available
            db.session.commit()
            return jsonify({"Message": "Parameter has been updated Successfully.", "ProcessName": f"{parameter_name}"}), 200
        else:
            return  jsonify({'Message':'Parameter does not exists'}) , 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to fetch records {e}'}), 422


def add_checksheet(data):
    try:
        csp_id = data.get('csp_id')
        csp_name = data.get('csp_name')
        specification = data.get('specification')
        control_method = data.get('control_method')
        frequency = data.get('frequency')
        csp_name_hindi = data.get('csp_name_hindi')
        added_by_owner = data.get('added_by_owner')
        
        exist_parameter_id = check_sheet.query.filter_by(csp_id=csp_id).first()
        if exist_parameter_id:
            return  jsonify({"Message": "Parameter has been already added"}), 304
        else:
            new_parameter = check_sheet(csp_id=csp_id, csp_name=csp_name, specification=specification, control_method=control_method, frequency=frequency, csp_name_hindi=csp_name_hindi, added_by_owner=added_by_owner)
            db.session.add(new_parameter)
            db.session.commit()
            return jsonify({"Message": "Data Added Successfully","Id":csp_id,"Name":csp_name}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def assign_task(data):
    try:
        current_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
        current_date = datetime.now(pytz.timezone('Asia/Kolkata')).date()
        assigned_task_stations = {}
        running_task_stations = {}
        # username = kwargs["token_payload"][1]['username']
        for stationTask in data:
            station_id = stationTask.get('station_id')
            print(station_id)
            employee_id = stationTask.get('employee_id')
            part_no = stationTask.get('part_no')
            process_no = stationTask.get('process_no')
            start_shift_time = stationTask.get('start_shift_time')
            end_shift_time = stationTask.get('end_shift_time')
            shift = stationTask.get('shift')
            assigned_by_owner = stationTask.get('assigned_by_owner')
            total_assigned_task = stationTask.get('total_assigned_task')

            # date = datetime.now().date()
            station = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
            if station:
                if station.end_shift_time>=current_time and station.date==current_date:
                    running_task_stations[station_id] = "Task is running on this station"
                    # return jsonify({"Message":"Task is running on this station"}), 200
                elif station.end_shift_time<current_time or station.date!=current_date:
                    # response[station_id] = "Please reset the all task first on this station"
                    db.session.rollback()
                    return jsonify({'Message': 'Please reset the all task first'}), 200
            else:
                ####################### this data will retrieve from privious date in work_assigned_to_operator_logs table#################
                left_for_rework = 0
                assign_task_obj = work_assigned_to_operator(employee_id=employee_id, station_id=station_id, part_no=part_no, process_no=process_no, start_shift_time=start_shift_time, end_shift_time=end_shift_time, shift=shift, assigned_by_owner=assigned_by_owner, total_assigned_task=total_assigned_task, left_for_rework=left_for_rework)
                db.session.add(assign_task_obj)
                db.session.commit()
                # return jsonify({'Message:': "Task assigned successfully to station!"}), 200
                assigned_task_stations[station_id] = "Task assigned successfully to station"
        return jsonify({'assigned task to': assigned_task_stations, 'running task to stations': running_task_stations}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def stations_info(data):
    try:
        floor_no = data.get('floor_no')
        print(floor_no)
        all_stations = []

        current_lines_data = stations.query.filter_by(floor_no=floor_no).all()
        # print(current_lines_data)
        if current_lines_data:
            for entity in range(0, len(current_lines_data)):
                all_stations.append(current_lines_data[entity].station_id)
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
                    
            return jsonify({'totalLines':f'{len(stations_dict)}', 'lines':f'{list(stations_dict)}', 'All_stations':f'{stations_dict}'}), 200
        else:
            return jsonify({"Message":"Employess datas does not exist."}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def stations_current_status():
    try:
        all_stations_status = db.session.query(work_assigned_to_operator.station_id, work_assigned_to_operator.failed, work_assigned_to_operator.passed, work_assigned_to_operator.filled, work_assigned_to_operator.shift, work_assigned_to_operator.start_shift_time, work_assigned_to_operator.end_shift_time).all()
        all_stations_data = [{'station_id': station_id, 'failed': failed, 'passed': passed, 'filled': filled, 'shift': shift, 'start_shift_time': str(start_shift_time), 'end_shift_time': str(end_shift_time)} for station_id, failed, passed, filled, shift, start_shift_time, end_shift_time in all_stations_status]
        # print(all_stations_data)
        return jsonify({"all_stations_data": all_stations_data})
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def refresh_data():
    try:
        station_ids = ['G01 F01 L04 S03', 'G01 F01 L04 S02', 'G01 F01 L04 S05']
        
        # Querying the database for records where the station_id matches any in the list
        matched_stations = db.session.query(work_assigned_to_operator).filter(work_assigned_to_operator.station_id.in_(station_ids)).all()
        # print(matched_stations[0].employee_id)
        if matched_stations:
            employee_ids = []
            for station_data in matched_stations:
                employee_ids.append(station_data.employee_id)
                # print(employee_ids)
            get_employees_data = db.session.query(Operator_creds).filter(Operator_creds.employee_id.in_(employee_ids)).all()
            datas = {}
            if get_employees_data:
                for employee_data in get_employees_data:
                #     print(datas)
                #     datas[station_data.employee_id].append({employee_data.fName, employee_data.lName, employee_data.skill_level})
                # Ensure a list exists for this employee_id, then extend it
                    if employee_data.employee_id not in datas:
                        datas[employee_data.employee_id] = []
                    datas[employee_data.employee_id].append({
                        'fName': employee_data.fName,
                        'lName': employee_data.lName,
                        'skill_level': employee_data.skill_level
                    })
                return jsonify({"Datas":f"{datas}"}), 200
            else:
                return jsonify({"Message":"Employess datas does not exist."}), 404
        else:
            return jsonify({"Message":"Stations datas does not exist."}), 404
        return jsonify({'h':'hiiii'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def free_stations_if_task_completed(data):
    try:
        station_id = data.get('station_id')
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        
        get_station_data = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
        if get_station_data:
            if get_station_data.end_shift_time>=current_time and get_station_data.date==current_date:
                return jsonify({"Message":"Task is running on this station"}), 200
            elif get_station_data.end_shift_time<current_time or get_station_data.date!=current_date:
                new_record = work_assigned_to_operator_logs(employee_id = get_station_data.employee_id,
                        station_id = get_station_data.station_id,
                        part_no = get_station_data.part_no,
                        process_no = get_station_data.process_no,
                        start_shift_time = get_station_data.start_shift_time,
                        end_shift_time = get_station_data.employee_id,
                        shift = get_station_data.shift,
                        # operator_login_status = get_station_data.operator_login_status,
                        total_assigned_task = get_station_data.total_assigned_task,
                        left_for_rework = get_station_data.left_for_rework,
                        passed = get_station_data.passed,
                        filled = get_station_data.filled,
                        failed = get_station_data.failed,
                        assigned_by_owner = get_station_data.assigned_by_owner)
                db.session.add(new_record)
                db.session.commit()
                
                db.session.delete(get_station_data)
                db.session.commit()
                
                return jsonify({"Message":"Stations is free now"}), 201
            else:
                return jsonify({"Message":"Stations has not assigned any task"}), 404
        else:
            return jsonify({"Message":"Stations has not assigned any task"}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def get_notification_info(data):
    try:
        floor_no = data.get("floor_no")
        all_notifications = notify_to_incharge.query.filter_by(floor_no=floor_no).all()
        all_csp_datas = db.session.query(check_sheet).all()
        notifications = []
        for notification in all_notifications:
            csp_id = notification.csp_id
            for csp_data in all_csp_datas:
                if csp_data.csp_id == csp_id:
                    csp_name = csp_data.csp_name
                
            notifications.append({
                "station_id": notification.station_id,
                "csp_name": csp_name,
                "csp_id": notification.csp_id,
                "created_at": str(notification.created_at)
            })
            
        if len(notifications) > 0:
            return jsonify( {"Notifications": notifications} ), 200
        else:
            return jsonify({"Message": "No Notifications Found"}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
        

def get_fpa_history(data):
    date = data.get('date')
    line_no = data.get('line_no')


def get_last_date_data(data):
    try:
        date = datetime.now().date()
        for count in range(1,28):
            minus_date = date - timedelta(days=count)
            find_data_by_date = work_assigned_to_operator_logs.query.filter_by(date=minus_date).all()
            if find_data_by_date:
                break
            else:
                continue
        
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422