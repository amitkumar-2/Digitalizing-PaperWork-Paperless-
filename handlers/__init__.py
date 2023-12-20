from flask import Flask, jsonify
import jwt
from datetime import datetime, timedelta
# from .FloorIncharge import FloorIncharge1
from .FloorIncharge.FloorIncharge import FloorIncharge1
from .Operator.Operator import Operator1
from pytz import timezone


# def return_flask_app():
#     app = Flask(__name__)
#     app.config["SECRET_KEY"] = "nie83jdie98239A9J3H4hdncHSJD8473"
#     return app

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "nie83jdie98239A9J3H4hdncHSJD8473"
    
    app.register_blueprint(FloorIncharge1)
    app.register_blueprint(Operator1)
    return app

# def create_tocken(username):
#     # app = return_flask_app()
#     app = create_app()
#     token = jwt.encode({
#         'user': username,
#         'expiration': str(datetime.utcnow() + timedelta(seconds=120))
#     }, app.config['SECRET_KEY'])
    
#     # return jsonify({'token': token.decode('utf-8')})
#     return jsonify({'token': token})
#     # print(token)











from flask import Flask, jsonify
import jwt
from datetime import datetime, timedelta
from pytz import timezone

# from .FloorIncharge import FloorIncharge1

# def create_tocken(username):
#     app = create_app()  # Assuming create_app() is defined somewhere

#     # Get the current time in UTC
#     current_utc_time = datetime.utcnow()
    
#     # Define the IST timezone
#     ist_timezone = timezone('Asia/Kolkata')  # IST is UTC+5:30

#     # Convert the current UTC time to IST
#     current_ist_time = current_utc_time.astimezone(ist_timezone)

#     # Set the expiration time to 120 seconds in the future in IST
#     expiration_time_ist = current_ist_time + timedelta(seconds=120)
    
#     # Print the expiration time for debugging
#     print("Token Expiry Time:", expiration_time_ist)

#     # Encode the JWT token
#     token = jwt.encode({
#         'user': username,
#         'exp': expiration_time_ist,  # 'exp' is the standard claim for expiration time
#     }, app.config['SECRET_KEY'], algorithm='HS256')
    
#     # print(type(token))
#     return jsonify({'token': token})

# # Example of decoding and verifying the token
# def decode_and_verify_token(token):
#     app = create_app()
#     try:
#         # If the token is a string, convert it to bytes before decoding
#         print(token)
#         if isinstance(token, str):
#             token = token.encode('utf-8')
#             print(token)
#         decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#         print(type(token))
#         print("Decoded Token:", decoded_token)
#         return decoded_token
#     except jwt.ExpiredSignatureError as e:
#         print("Token has expired", e)
#         return None

# # Example of checking token expiration
# def is_token_expired(token):
#     decoded_token = decode_and_verify_token(token)
#     if decoded_token:
#         expiration_time = datetime.utcfromtimestamp(decoded_token['exp'])
#         print(expiration_time)
#         current_utc_time = datetime.utcnow()
#         print(current_utc_time)
#         return expiration_time <= current_utc_time
#     return True






def create_tocken(username, user_id):
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=5),
    }
    app = create_app()
    # Encode the JWT token
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS512')

def decode_and_verify_token(token):
    app = create_app()
    try:
        # If the token is a string, convert it to bytes before decoding
        if isinstance(token, str):
            token = token.encode('utf-8')
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS512'])
        print("Decoded Token:", decoded_token)
        return decoded_token
    except jwt.ExpiredSignatureError as e:
        print("Token has expired:", e)
        return None
    except jwt.DecodeError as e:
        print("Error decoding token:", e)
        return None

def is_token_expired(token):
    decoded_token = decode_and_verify_token(token)
    if decoded_token:
        expiration_time = datetime.utcfromtimestamp(decoded_token['exp'])
        current_utc_time = datetime.utcnow()
        print(expiration_time, current_utc_time)
        return expiration_time <= current_utc_time
    return True