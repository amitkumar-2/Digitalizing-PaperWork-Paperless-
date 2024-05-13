from flask import request, jsonify, session, current_app
import pytz
from Database.init_and_conf import db
from Database.models import floor_incharge_creds, Operator_creds, parts_info, processes_info, parameters_info, check_sheet_data, stations, work_assigned_to_operator, work_assigned_to_operator_logs, check_sheet, notify_to_incharge, check_sheet_data_logs, fpa_and_set_up_approved_records, fpa_and_set_up_approved_records_logs, reading_params, reading_params_logs, reasons
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
            return jsonify({'Response:': "Operator User added successfully!"}), 201
        else:
            return jsonify( {"Response":"User already exists."} ), 200
    except Exception as e:
        return jsonify({"Error in adding data":f"Some error occurred while adding the data to the database: {e}"}), 422

def operator_change_password(data):
    try:
        employee_id = data.get('employee_id')
        password = data.get('password')
        
    except:
        return jsonify({"Error": "Username and Password Not Defined"})
    
    try:
        user = Operator_creds.query.filter_by(employee_id=employee_id).first()
        if user:
            user.password = password or user.password
            db.session.commit()
            return jsonify({'Response:': "Operator Password updated successfully!"}), 201
        else:
            return jsonify( {"Response":"User does't exists."} ), 404
    except Exception as e:
        return jsonify({"Error in adding data":f"Some error occurred while adding the data to the database: {e}"}), 422

def get_operator_details(data):
    try:
        employee_id = data.get("employee_id")

        operator_details_data = Operator_creds.query.filter_by(employee_id=employee_id).first()

        if operator_details_data is not None:
            result = {}
            result['Employee ID'] = operator_details_data.employee_id
            result["First Name"] = operator_details_data.fName
            result["Middle Name"] = operator_details_data.mName
            result["Last Name"] = operator_details_data.lName
            result["Skill Level"] = operator_details_data.skill_level
            result["Date of Birth"] = operator_details_data.dob.strftime("%B %d, %Y")
            result["Mobile Number"] = operator_details_data.mobile
            result["Email"] = operator_details_data.email
            return jsonify(result), 200
        else:
            return jsonify({"Message": "No Details Found for the Employee Id Provided"}),404
    except Exception as e:
        return jsonify({"Error in adding data":f"Some error occurred while adding the data to the database: {e}"}), 422

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
                    {'process_name': process.process_name, 'process_no': process.process_no, 'skill_level': process.required_skill_level}
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
                    return jsonify({"data": parameters_data}), 200
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

def add_stations(data_list):
    responses = []
    try:
        for data in data_list:
            station_id = data.get('station_id')
            line_no = data.get('line_no')
            floor_no = data.get('floor_no')
            building_no = data.get('building_no')
            location = data.get('location')
            added_by_owner = data.get('added_by_owner')

            # Check if the line number exists
            # if not stations.query.filter_by(station_id=station_id).first():
            #     responses.append({"station_id": station_id, "message": "Line does not exist."})
            #     continue
            
            # Check if the station ID already exists on any line
            if stations.query.filter_by(station_id=station_id).first():
                responses.append({"station_id": station_id, "message": "This station number already exists."})
                continue

            # Create new station
            new_station = stations(
                station_id=station_id,
                line_no=line_no,
                floor_no=floor_no,
                building_no=building_no,
                location=location,
                added_by_owner=added_by_owner
            )
            db.session.add(new_station)
            responses.append({"station_id": station_id, "message": "New station has been added successfully."})

        # Commit all valid entries to the database
        db.session.commit()
        return jsonify(responses), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error occurred: {str(e)}'}), 422
        

def assign_task(data):
    try:
        current_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
        current_date = datetime.now(pytz.timezone('Asia/Kolkata')).date()
        assigned_task_stations = {}
        running_task_stations = {}
        operator_assigned_station = {}
        last_shift_on_these_stations = {}
        # username = kwargs["token_payload"][1]['username']
        for stationTask in data:
            station_id = stationTask.get('station_id')
            # print(station_id)
            employee_id = stationTask.get('employee_id')
            part_no = stationTask.get('part_no')
            process_no = stationTask.get('process_no')
            start_shift_time = stationTask.get('start_shift_time')
            end_shift_time = stationTask.get('end_shift_time')
            shift = stationTask.get('shift')
            assigned_by_owner = stationTask.get('assigned_by_owner')
            total_assigned_task = stationTask.get('total_assigned_task')
            
            past_shift_of_station = work_assigned_to_operator_logs.query.filter_by(station_id=station_id, assigned_date=current_date).first()
            if past_shift_of_station:
                if shift == past_shift_of_station.shift:
                    print("##printing shift", (past_shift_of_station.shift))
                    last_shift_on_these_stations[past_shift_of_station.station_id] = shift
                    continue
            
            # date = datetime.now().date()
            employee_data = work_assigned_to_operator.query.filter_by(employee_id=employee_id).first()
            if employee_data:
                if station_id in operator_assigned_station:
                    operator_assigned_station[employee_id].append(employee_data.station_id)
                    continue
                else:
                    operator_assigned_station[employee_id]=[employee_data.station_id]
                    continue
                # jsonify({'Message': f'Operator has assigned task on {employee_data.station_id}'})

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
                assign_task_obj = work_assigned_to_operator(employee_id=employee_id, station_id=station_id, part_no=part_no, process_no=process_no, start_shift_time=start_shift_time, end_shift_time=end_shift_time, shift=shift, assigned_by_owner=assigned_by_owner, total_assigned_task=total_assigned_task)
                db.session.add(assign_task_obj)
                db.session.commit()
                # return jsonify({'Message:': "Task assigned successfully to station!"}), 200
                assigned_task_stations[station_id] = "Task assigned successfully to station"
        return jsonify({'assigned task to': assigned_task_stations, 'running task to stations': running_task_stations, "operator_assigned_to_stations": operator_assigned_station, "last_shift_on_these_stations": last_shift_on_these_stations}), 200
        
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
def apply_filters(filter_criteria):
    try:
        floor_no1 = filter_criteria.encode('utf-8').decode('utf-8').strip()
        # floor_no1 = filter_criteria
        # floor_no = 'G01 F02'
        # print("#################", repr(floor_no1))
        # print("#################", repr(floor_no))
        stations_datas = stations.query.filter_by(floor_no=floor_no1).all()
        print("####", stations_datas)
        global all_stations_data
        all_stations_data = []
        for entity in stations_datas:
            station_data = work_assigned_to_operator.query.filter_by(station_id=entity.station_id).first()
            if station_data:
                all_stations_data.append({'station_id': station_data.station_id, 'failed': station_data.failed, 'passed': station_data.passed, 'filled': station_data.filled, 'shift': station_data.shift, 'start_shift_time': str(station_data.start_shift_time), 'end_shift_time': str(station_data.end_shift_time)})
            else:
                pass
        return all_stations_data
    except Exception as e:
        print(f'Error applying filters: {e}')
        return []


def refresh_data(data):
    try:
        stations_ids = data.get("stations_ids", [])
        
        # Querying the database for records where the station_id matches any in the list
        matched_stations = db.session.query(work_assigned_to_operator).filter(work_assigned_to_operator.station_id.in_(stations_ids)).all()

        if matched_stations:
            employee_to_station_map = {}
            employee_ids = []

            datas = {}

            # Collect employee_ids and map them to station_ids
            for station_data in matched_stations:
                employee_ids.append(station_data.employee_id)
                employee_to_station_map[station_data.employee_id] = station_data.station_id

            get_employees_data = db.session.query(Operator_creds).filter(Operator_creds.employee_id.in_(employee_ids)).all()

            if get_employees_data:
                for employee_data in get_employees_data:
                    # Get the station_id corresponding to the employee_id
                    station_id = employee_to_station_map[employee_data.employee_id]
                    
                    employee_info = {
                        'fName': employee_data.fName,
                        'lName': employee_data.lName,
                        'skill_level': employee_data.skill_level,
                        'parts_no': matched_stations[employee_ids.index(employee_data.employee_id)].part_no,  # Get part_no from matched_stations
                        'process_no': matched_stations[employee_ids.index(employee_data.employee_id)].process_no  # Get process_no from matched_stations
                    }
                    if station_id not in datas:
                        datas[station_id] = []
                    datas[station_id].append(employee_info)
                    # datas[station_id]['employees'].append(employee_info)

                return jsonify({"Datas": datas}), 200
            else:
                return jsonify({"Message": "Employees data does not exist."}), 404
        else:
            return jsonify({"Message": "Stations data does not exist."}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422


def free_stations_if_task_completed(data):
    try:
        stations_ids = data.get("stations_ids", [])
        # station_id = data.get('station_id')
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        
        task_running_on_stations = []
        free_stations = []
        stations_not_any_task = []
        
        for station_id in stations_ids:
            get_station_data = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
            get_station_check_sheet_data = check_sheet_data.query.filter_by(station_id=station_id).first()
            get_fpa_data = fpa_and_set_up_approved_records.query.filter_by(station_id=station_id).first()
            station_readings_entities = reading_params.query.filter_by(station_id=station_id).all()
            if get_station_data:
                if get_station_data.end_shift_time>=current_time and get_station_data.date==current_date:
                    process_data = processes_info.query.filter_by(process_no=get_station_data.process_no).first()
                    operator_name = Operator_creds.query.filter_by(employee_id=get_station_data.employee_id).first()
                    task_running_on_stations.append([get_station_data.station_id, get_station_data.employee_id, operator_name.fName, operator_name.lName, operator_name.skill_level, get_station_data.process_no, process_data.required_skill_level])
                elif get_station_data.end_shift_time<current_time or get_station_data.date!=current_date:
                    new_record = work_assigned_to_operator_logs(employee_id = get_station_data.employee_id,
                            station_id = get_station_data.station_id,
                            part_no = get_station_data.part_no,
                            process_no = get_station_data.process_no,
                            start_shift_time = get_station_data.start_shift_time,
                            end_shift_time = get_station_data.end_shift_time,
                            shift = get_station_data.shift,
                            # operator_login_status = get_station_data.operator_login_status,
                            total_assigned_task = get_station_data.total_assigned_task,
                            check_fpa_status_at = get_station_data.check_fpa_status_at,
                            passed = get_station_data.passed,
                            filled = get_station_data.filled,
                            failed = get_station_data.failed,
                            assigned_by_owner = get_station_data.assigned_by_owner,
                            assigned_date = get_station_data.date)
                    try:
                        new_check_sheet_record = check_sheet_data_logs(station_id=get_station_check_sheet_data.station_id,
                                                                    oprtr_employee_id=get_station_check_sheet_data.oprtr_employee_id,
                                                                    flrInchr_employee_id=get_station_check_sheet_data.flrInchr_employee_id,
                                                                    status_datas=get_station_check_sheet_data.status_datas)
                    except:
                        new_check_sheet_record = check_sheet_data_logs(station_id=get_station_data.station_id,
                                                                    oprtr_employee_id=get_station_data.employee_id,
                                                                    flrInchr_employee_id=get_station_data.assigned_by_owner,
                                                                    status_datas="Checksheet Not Filled")
                    try:
                        new_fpa_data_logs = fpa_and_set_up_approved_records_logs(station_id=get_fpa_data.station_id, start_shift_1_parameters_values=get_fpa_data.start_shift_1_parameters_values, start_shift_1_time=get_fpa_data.start_shift_1_time, start_shift_2_parameters_values=get_fpa_data.start_shift_2_parameters_values, start_shift_2_time=get_fpa_data.start_shift_2_time, end_shift_1_parameters_values=get_fpa_data.end_shift_1_parameters_values, end_shift_1_time=get_fpa_data.end_shift_1_time, end_shift_2_parameters_values=get_fpa_data.end_shift_2_parameters_values, end_shift_2_time=get_fpa_data.end_shift_2_time, date=get_fpa_data.date, logs_date=current_date)
                    except:
                        new_fpa_data_logs = fpa_and_set_up_approved_records_logs(station_id=station_id, logs_date=current_date)
                    
                    try:
                        if station_readings_entities:
                            reading_param_logs_list = []
                            for entity in station_readings_entities:
                                new_readings_data_logs = reading_params_logs(parameter_no=entity.parameter_no, reading_1=entity.reading_1, reading_1_time=entity.reading_1_time, reading_2=entity.reading_2, reading_2_time=entity.reading_2_time, reading_3=entity.reading_3, reading_3_time=entity.reading_3_time, reading_4=entity.reading_4, reading_4_time=entity.reading_4_time, reading_5=entity.reading_5, reading_5_time=entity.reading_5_time, station_id=entity.station_id, shift=get_station_data.shift, date=entity.date, logs_date=current_date)
                                
                                reading_param_logs_list.append(new_readings_data_logs)
                        else:
                            pass
                    except Exception as e:
                        print("This is an error: ", e)
                    
                    
                    if station_readings_entities:
                        for entity_data  in reading_param_logs_list:
                            db.session.add(entity_data)
                        # db.session.commit()

                        for  remove_data in station_readings_entities:
                            db.session.delete(remove_data)
                        # db.session.commit()
                    else:
                        pass
                    
                    db.session.add(new_fpa_data_logs)
                    # db.session.commit()
                    
                    db.session.add(new_check_sheet_record)
                    # db.session.commit()

                    db.session.add(new_record)
                    # db.session.commit()
                    
                    if get_fpa_data:
                        db.session.delete(get_fpa_data)
                        # db.session.commit()
                    else:
                        pass
                    
                    if get_station_check_sheet_data:
                        db.session.delete(get_station_check_sheet_data)
                        # db.session.commit()
                    else:
                        pass
                    
                    db.session.delete(get_station_data)
                    db.session.commit()
                
                    free_stations.append(get_station_data.station_id)
                else:
                    # return jsonify({"Message":"Stations has not assigned any task"}), 404
                    pass
                
                
                
            else:
                # return jsonify({"Message":"Stations has not assigned any task"}), 404
                pass    
        return jsonify({"task_running_on_stations": task_running_on_stations, "free_stations": free_stations}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
    finally:
        # Ensure the session is closed properly
        db.session.close()

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
                "notification_id": notification.notification_id,
                "station_id": notification.station_id,
                "csp_name": csp_name,
                "csp_id": notification.csp_id,
                "created_date": str(notification.created_date),
                "created_time": str(notification.created_time)
            })
            
        if len(notifications) > 0:
            return jsonify( {"Notifications": notifications} ), 200
        else:
            return jsonify({"Message": "No Notifications Found"}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def delete_notification(data):
    try:
        notification_id = data.get("notification_id")
        
        add_notification = notify_to_incharge.query.filter_by(notification_id=notification_id).first()
        db.session.delete(add_notification)
        db.session.commit()
        return jsonify({"Message":f"Notification sent to in-charge for Station ID :{notification_id}"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

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


def get_floor_data(data):
    try:
        floor_no = data.get('floor_no')
        # building, floor = floor_no.split(' ')
        all_lines_stations=[]

        # Fetch all station_ids for the given floor_no
        current_lines_data = stations.query.filter_by(floor_no=floor_no).all()
        print(current_lines_data)
        if current_lines_data:
            for entity in range(0, len(current_lines_data)):
                all_lines_stations.append(current_lines_data[entity].station_id)
            # all_duplicates = dict(Counter(all_stations))
            all_lines_stations.sort()
            # Create a dictionary to store the results
            stations_dict = {}
            
            all_stations = [entity.station_id for entity in current_lines_data]
            print(all_stations)

            # Create a dictionary to store the results
            result = {} 
            operator_data = {}
            for station in all_lines_stations:
                prefix = station.rsplit(' S', 1)[0]
                # Add the station to the list associated with the prefix in the dictionary
                if prefix in stations_dict:
                    stations_dict[prefix].append(station)
                else:
                    stations_dict[prefix] = [station]

            # Iterate over each station_id and fetch data from work_operator table
            for station_id in all_stations:
                
                operator_data = work_assigned_to_operator.query.filter_by(station_id=station_id).all()
                print(operator_data)
                if operator_data:
                    station_result = []
                    for op in operator_data:
                        employee_data = Operator_creds.query.filter_by(employee_id=op.employee_id).first()
                        if employee_data:
                            station_result.append({
                                'station_id': op.station_id,
                                'part_no': op.part_no,
                                'process_no': op.process_no,
                                'employee_id': op.employee_id,
                                'total_assigned_task': op.total_assigned_task,
                                'employee_name': employee_data.fName,
                                'employee_skill_level': employee_data.skill_level
                            })
                    result[station_id] = station_result
                else:
                    result[station_id]=[]
            
            parts = db.session.query(parts_info.part_no, parts_info.part_name).all()

# Fetch process info based on part_no
            parts_data = []
            for part_no, part_name in parts:
                process_info = db.session.query(processes_info.process_no, processes_info.process_name).filter_by(belongs_to_part=part_no).all()

    # Format process info and add part_no
                process_data = [{'process_no': process_no, 'process_name': process_name}
                    for process_no, process_name in process_info]

                parts_data.append({'part_name': part_name, 'part_no': part_no, 'process_data': process_data})
            
            employee_data = db.session.query(Operator_creds.employee_id, Operator_creds.fName, Operator_creds.mName, Operator_creds.lName , Operator_creds.skill_level).all()

            formatted_employee_data = [{'employee_id': employee_id, 'employee_name': f"{fName} {mName} {lName}", 'skill_level':skill_level} for employee_id, fName, mName, lName, skill_level in employee_data]

                # ######################process skill add hogi abhi ########################################

            return jsonify({"station_data":result,"parts_data":parts_data,'totalLines':f'{len(stations_dict)}', 'lines':f'{list(stations_dict)}', 'All_stations':f'{stations_dict}' , 'formatted_employee_data':formatted_employee_data}), 200
        else:
            return jsonify({"Message": "No stations found for the given floor_no."}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Failed to fetch data: {e}'}), 500

def  get_stations_previous_data(data):
    try:
        floor_no = data.get("floor_no")
        assigned_date = data.get("date")
        time_str = data.get("time")
        # Convert string to datetime.time object
        time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
        
        previous_stations_data = {}
        running_task_on_stations = []
        
        get_stations = stations.query.filter_by(floor_no=floor_no).all()
        if get_stations:
            for entity in range(0, len(get_stations)):
                station_id = get_stations[entity].station_id
                running_task_on_station = work_assigned_to_operator.query.filter_by(station_id=station_id).first()
                if running_task_on_station:
                    process_data = processes_info.query.filter_by(process_no=running_task_on_station.process_no).first()
                    operator_name = Operator_creds.query.filter_by(employee_id=running_task_on_station.employee_id).first()
                    running_task_on_stations.append([running_task_on_station.station_id, running_task_on_station.employee_id, operator_name.fName, operator_name.lName, operator_name.skill_level, running_task_on_station.process_no, process_data.required_skill_level])
                    continue
                # latest_data = work_assigned_to_operator_logs.query.filter_by(station_id=station_id, date=date).order_by(db.desc(work_assigned_to_operator_logs.date)).first()
                latest_datas = work_assigned_to_operator_logs.query.filter_by(station_id=station_id, assigned_date=assigned_date).all()
                if latest_datas:
                    for i in range(0, len(latest_datas)):
                        if latest_datas[i].start_shift_time <= time_obj <= latest_datas[i].end_shift_time:
                            latest_data =  latest_datas[i]
                            process_data = processes_info.query.filter_by(process_no=latest_data.process_no).first()
                            # break
                        # if latest_data:
                            operator_name = Operator_creds.query.filter_by(employee_id=latest_data.employee_id).first()
                            if operator_name:
                                previous_stations_data[station_id] = [operator_name.fName]
                                previous_stations_data[station_id].append(operator_name.lName)
                                previous_stations_data[station_id].append(operator_name.skill_level)
                                previous_stations_data[station_id].append(latest_data.part_no)
                                previous_stations_data[station_id].append(latest_data.process_no)
                                previous_stations_data[station_id].append(process_data.required_skill_level)
                                previous_stations_data[station_id].append(latest_data.employee_id)
                            else:
                                jsonify({"Message": "By-mistake operator doesn't exist, Please contact database admin..."}), 404
                else:
                    jsonify({"Message": "Not matched data found"}), 404
            return jsonify({"Datas": previous_stations_data, "running_task_on_stations": running_task_on_stations}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

################################ failed items reason functions ##############################
def add_reason(data):
    try:
        reason = data.get('reason')
        floor_no=data.get('floor_no')
        floor_incharge_id=data.get('floor_incharge_id')
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        if len(reason)<=0:
            return jsonify({'Error': 'Reason is required'}), 422
        if len(floor_no)<=0:
            return jsonify({'Error':'Floor_no is required'}), 422
        if len(floor_incharge_id)<=0:
            return jsonify({'Error':'Floor_incharge_id is required'}), 422
        reason_for_parts = reasons(reason=reason,floor_no=floor_no,floor_incharge_id=floor_incharge_id,date=current_date,time=current_time)
        db.session.add(reason_for_parts)
        db.session.commit()
        return jsonify({'Message': 'Reason for parts added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422

def get_reasons_for_items(data):
    try:
        floor_no=data.get('floor_no')
        if floor_no:
            exist_reasons= reasons.query.filter_by(floor_no=floor_no).all()
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

def delete_reason_for_items(data):
    try:
        reason_id=data.get('reason_id')
        reason = reasons.query.filter_by(reason_id=reason_id).first()
        if reason:
            db.session.delete(reason)
            db.session.commit()
            return jsonify({"Message": f"Reason with reason_id {reason_id} deleted successfully."}), 200
        else:
            return jsonify({"Message": f"No reason found with reason_id {reason_id}."}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Failed to delete reason: {e}'}), 500

#####################################################################################################################################
############################################### get previous data and api for history ###############################################
#####################################################################################################################################

def get_readings_for_chart(data):
    row_start_date = data.get('start_date')
    row_end_date = data.get('end_date')
    
    
    start_date = datetime.strptime(row_start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(row_end_date, '%Y-%m-%d').date()
    
    # Calculate the difference between dates
    date_difference = (end_date - start_date).days
    if date_difference > 46:
        return  jsonify({"Message":"Your given date difference is more than 45 days"}), 403
    
    parameter_no = data.get('parameter_no')
    
    readings_data = {}
    
    station_readings_data = {}
    

    results = reading_params_logs.query.filter(
        reading_params_logs.date.between(start_date, end_date),
        reading_params_logs.parameter_no == parameter_no
        ).paginate(per_page=200) #paginate(page, per_page, False)#yield_per(2) #.all()
    
    for entity in (results.items):
        date = str(entity.date)
        station_id = entity.station_id
        shift = entity.shift
        
        if date in readings_data:
            pass
        else:
            readings_data[date]  = {}
        # if station_id in station_readings_data:
        #     pass
        # else:
        #     station_readings_data[station_id] = []
        
        if station_id in readings_data[date]:
            pass
        else:
            readings_data[date][station_id] = {}
        
        if shift in readings_data[date][station_id]:
            pass
        else:
            readings_data[date][station_id][shift] = []
            
            readings_data[date][station_id][shift].extend([
            entity.reading_1,
            entity.reading_2,
            entity.reading_3,
            entity.reading_4,
            entity.reading_5
           ])
        # # station_readings_data[station_id].append(entity.station_id)
        # station_readings_data[station_id].append(entity.reading_1)
        # # station_readings_data[station_id].append(str(entity.reading_1_time))
        # station_readings_data[station_id].append(entity.reading_2)
        # station_readings_data[station_id].append(entity.reading_3)
        # station_readings_data[station_id].append(entity.reading_4)
        # station_readings_data[station_id].append(entity.reading_5)
        # # station_readings_data[station_id].append(str(entity.reading_5_time))
        # readings_data[date] = station_readings_data
    return jsonify({"result": readings_data}), 200
    
    


def station_history(data):
    try:
        station_id = data.get("station_id")
        date = datetime.now().date()
        
        station_previous_data = work_assigned_to_operator_logs.query.filter_by(station_id=station_id, date=date)

        if station_previous_data:
            employee_id = station_previous_data.employee_id
            part_no = station_previous_data.part_no
            process_no = station_previous_data.process_no
            start_shift_time = station_previous_data.start_shift_time
            end_shift_time = station_previous_data.end_shift_time
            shift = station_previous_data.shift
            assigned_by_owner = station_previous_data.assigned_by_owner
            total_assigned_task = station_previous_data.total_assigned_task
            check_fpa_status_at = station_previous_data.check_fpa_status_at
            passed = station_previous_data.passed
            filled = station_previous_data.filled
            failed = station_previous_data.failed

        

        #         return jsonify({"Datas": datas}), 200
        #     else:
        #         return jsonify({"Message": "Employees data does not exist."}), 404
        # else:
        #     return jsonify({"Message": "Stations data does not exist."}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422