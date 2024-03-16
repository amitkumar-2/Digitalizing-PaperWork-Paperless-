from flask import Flask, jsonify, request
from functools import wraps
import jwt
from datetime import datetime, timedelta
# from .FloorIncharge import FloorIncharge1
from .FloorIncharge.FloorIncharge import FloorIncharge1
from .Operator.Operator import Operator1
from pytz import timezone


# def create_tocken(employee_id, mobile_no):
#     payload = {
#         'mobile_no': mobile_no,
#         'employee_id': employee_id,
#         'exp': datetime.utcnow() + timedelta(minutes=5),
#     }
#     app = create_app()
#     # Encode the JWT token
#     return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS512')

# def decode_and_verify_token(token):
#     app = create_app()
#     try:
#         # If the token is a string, convert it to bytes before decoding
#         if isinstance(token, str):
#             token = token.encode('utf-8')
#         decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS512'])
#         # print("Decoded Token:", decoded_token)
#         return decoded_token
#     except jwt.ExpiredSignatureError as e:
#         print("Token has expired:", e)
#         return None
#     except jwt.DecodeError as e:
#         print("Error decoding token:", e)
#         return None

# def is_token_expired(token):
#     decoded_token = decode_and_verify_token(token)
#     if decoded_token:
#         expiration_time = datetime.utcfromtimestamp(decoded_token['exp'])
#         current_utc_time = datetime.utcnow()
#         # print(expiration_time, current_utc_time)
#         return expiration_time <= current_utc_time, decoded_token
#     return True


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "nie83jdie98239A9J3H4hdncHSJD8473"
    
    app.register_blueprint(FloorIncharge1)
    app.register_blueprint(Operator1)
    return app


# class token_requirments:
#     def __init__(self):
#         pass
#     def create_tocken(employee_id, mobile_no):
#         payload = {
#             'mobile_no': mobile_no,
#             'employee_id': employee_id,
#             'exp': datetime.utcnow() + timedelta(minutes=5),
#         }
#         app = create_app()
#         # Encode the JWT token
#         return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS512')
#     def decode_and_verify_token(token):
#         app = create_app()
#         try:
#             # If the token is a string, convert it to bytes before decoding
#             if isinstance(token, str):
#                 token = token.encode('utf-8')
#             decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS512'])
#             # print("Decoded Token:", decoded_token)
#             return decoded_token
#         except jwt.ExpiredSignatureError as e:
#             print("Token has expired:", e)
#             return None
#         except jwt.DecodeError as e:
#             print("Error decoding token:", e)
#             return None
#     def is_token_expired(self, token):
#         decoded_token = self.decode_and_verify_token(token)
#         if decoded_token:
#             expiration_time = datetime.utcfromtimestamp(decoded_token['exp'])
#             current_utc_time = datetime.utcnow()
#             # print(expiration_time, current_utc_time)
#             return expiration_time <= current_utc_time, decoded_token
#         return True

#     def token_required(self, func):
#         @wraps(func)
#         def decorated(*args, **kwargs):
#             token = request.args.get('token')
#             if not token:
#                 return jsonify({'Alert!': 'Token is missing!'})
#             try:
#                 payload = self.is_token_expired(token)
#                 # Add the token payload to the kwargs so that it's available to the protected route
#                 kwargs['token_payload'] = payload
#                 if payload[0] == False:
#                     try:
#                         # Call the original function with the token payload
#                         return func(*args, **kwargs)
#                     except:
#                         return jsonify({"Error:": "An error occurred while trying to excute the function."})
#                 else:
#                     return jsonify({'Alert!': 'Token is expired!'})
#             except:
#                 return jsonify({'Alert!': 'Invalid Token!'})
#         return decorated



