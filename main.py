import eventlet
eventlet.monkey_patch()
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler
from Database import init_and_conf
# from Config.routes import generate_routes
from Config.creds import DevConfig
from Models.FloorIncharge.FloorIncharge import stations_current_status, apply_filters
# from handlers import FloorIncharge
# import handlers
# from Database import models

from handlers import create_app



app=create_app()
CORS(app, origins=["*"], supports_credentials=True)

# Add database
app.config['SQLALCHEMY_DATABASE_URI']=DevConfig.SQLALCHEMY_DATABASE_URI
# Secret Key
# app.config['SECRET_KEY'] = DevConfig.POSTGRES_SECRET_KEY
# Initializing Database
init_and_conf.db.init_app(app)
init_and_conf.migrate.init_app(app, init_and_conf.db)


# socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
socketio = SocketIO(app, cors_allowed_origins="*")
scheduler = BackgroundScheduler()


# # WebSocket event handler
# latest_result = {"all_stattions_data": None}

# latest_data = None


# # Method to update the latest data
# def update_latest_data():
#     global latest_data
#     response = stations_current_status()
#     # print(response)
#     result = response.json
#     # print(result)
#     latest_data = result['all_stations_data']

# # WebSocket event handler
# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')
#     # Update the latest data when a client connects
#     update_latest_data()
#     # Emit the latest data to the client
#     if latest_data is not None:
#         socketio.emit('update_work_for_operator', {'all_stations_data': latest_data})

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')


# # Background task for periodic updates
# def scheduled_task():
#     print("Entering scheduled_task")
#     with app.app_context():
#         global latest_data
#         try:
#             # print("latest_data:", latest_data)
#             update_latest_data()
#             if latest_data is not None:
#                 print("Emitting message to clients")
#                 socketio.emit('update_work_for_operator', {'all_stations_data': latest_data})
#             else:
#                 print("latest_data is empty...")
#         except Exception as e:
#             print(f"Error in scheduled_task: {e}")


# # Start the background task when the server starts
# scheduler.add_job(scheduled_task, 'interval', seconds=5)
# scheduler.start()




filters = {}  # Global dictionary to store user filters keyed by session ID

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('set_filter')
def handle_set_filter(data):
    session_id = request.sid
    filters[session_id] = data
    print(f"Filter set for {session_id}: {data}")
    # You can also send the latest filtered data right after setting the filter
    filtered_data = apply_filters(data)
    if filtered_data:
        socketio.emit('update_work_for_operator', {'all_stations_data': filtered_data}, room=session_id)


def scheduled_task():
    print("Entering scheduled_task")
    with app.app_context():
        try:
            for session_id, criteria in filters.items():
                filtered_data = apply_filters(criteria)
                if filtered_data:
                    print(f"Emitting filtered data to {session_id}")
                    socketio.emit('update_work_for_operator', {'all_stations_data': filtered_data}, room=session_id)
        except Exception as e:
            print(f"Error in scheduled_task: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in filters:
        del filters[session_id]
    print(f'Client disconnected {session_id}')


scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', seconds=5)
scheduler.start()





if __name__=="__main__":
    with app.app_context():
        init_and_conf.db.create_all()
    # app.run(host='0.0.0.0', port=5000)
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False)