from flask import Flask, jsonify
import jwt
from datetime import datetime, timedelta
from cricket.batsman import batsman1
from cricket.bowler import bowler1
from cricket.main import main1
from cricket.ChatGpt import bp

def return_flask_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "nie83jdie98239A9J3H4hdncHSJD8473"
    return app

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main1)
    app.register_blueprint(batsman1)
    app.register_blueprint(bowler1)
    app.register_blueprint(bp)

    return app


def create_tocken(username):
    app = return_flask_app()
    token = jwt.encode({
        'user': username,
        'expiration': str(datetime.utcnow() + timedelta(seconds=120))
    }, app.config['SECRET_KEY'])
    
    # return jsonify({'token': token.decode('utf-8')})
    print(token)

# create_tocken(username='amitkumar')