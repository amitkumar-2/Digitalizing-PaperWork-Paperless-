import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

from apscheduler.schedulers.background import BackgroundScheduler

def my_scheduled_task():
    print("Sending message to clients")
    socketio.emit('my event', {'data': 'Message from scheduled task'})

scheduler = BackgroundScheduler()
scheduler.add_job(my_scheduled_task, 'interval', seconds=10)
scheduler.start()

if __name__ == '__main__':
    socketio.run(app)
