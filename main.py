from flask import Flask
from datetime import datetime
from Database import init_and_conf
# from Config.routes import generate_routes
from Config.creds import DevConfig
from handlers import FloorIncharge
from Database import models

from handlers import create_app

# Create a flask Instance
# app=Flask(__name__)




# generate_routes(app)
# app.register_blueprint(FloorIncharge)

app=create_app()

# Add database
app.config['SQLALCHEMY_DATABASE_URI']=DevConfig.SQLALCHEMY_DATABASE_URI
# Secret Key
# app.config['SECRET_KEY'] = DevConfig.POSTGRES_SECRET_KEY
# Initializing Database
init_and_conf.db.init_app(app)
init_and_conf.migrate.init_app(app, init_and_conf.db)


# @app.route("/")
# def home():
#     return "Hello World!"


if __name__=="__main__":
    with app.app_context():
        init_and_conf.db.create_all()
    app.run(debug=True)