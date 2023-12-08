from flask import Blueprint, render_template, request, jsonify, make_response, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
# from cricket import create_tocken


main1 = Blueprint('main', __name__)

@main1.route("/main")
def main():
    return "<h1>This is main page</h1>"

@main1.route("/")
def home():
    if not session.get('logged_in'):
        return "Please Return Login Page"
    else:
        return "User Dashboard!"

@main1.route("/login", methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
    #     token = jwt.encode({
    #         'user': request.form['username'],
    #         'expiration': str(datetime.utcnow() + timedelta(seconds=120))
    #         }, 
    #                        app.config)
    
        # token = create_tocken(username='amitkumar')
    
        # return token