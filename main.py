from flask import Flask
from flask_cors import CORS
from datetime import datetime
from Database import init_and_conf
# from Config.routes import generate_routes
from Config.creds import DevConfig
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



if __name__=="__main__":
    with app.app_context():
        init_and_conf.db.create_all()
    app.run(host='0.0.0.0', port=5000)