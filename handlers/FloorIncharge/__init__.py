from flask import Blueprint, render_template, request, session, jsonify, make_response
import handlers
from functools import wraps

FloorIncharge1=Blueprint('FloorIncharge', __name__)



def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'})
        try:
            payload = handlers.is_token_expired(token)
            # Add the token payload to the kwargs so that it's available to the protected route
            kwargs['token_payload'] = payload
            
            if payload == False:
                # Call the original function with the token payload
                return func(*args, **kwargs)
            else:
                return jsonify({'Alert!': 'Token is expired!'})
        except:
            return jsonify({'Alert!': 'Invalid Token!'})
        
        
    
    return decorated

@FloorIncharge1.route('/public')
def public():
    return 'For Public'

@FloorIncharge1.route('/auth')
@token_required
def auth(**kwargs):
    return 'JWT is verified. Welcome to your Dashboard!'
# def auth(**kwargs):
#     token_payload = kwargs.get('token_payload')
#     print("##################", token_payload)
    
#     # Check if the token payload is available
#     if token_payload == False:
#         # return jsonify({'message': f'JWT is verified. Welcome to your Dashboard, {token_payload["user"]}!'})
#         return jsonify({'message': f'JWT is verified. Welcome to your Dashboard, {token_payload}!'})
#     else:
#         # The decorator has already handled the case where the token is missing or invalid
#         # This line will not be reached if the token is missing or invalid
#         return jsonify({'message': 'Authentication failed.'}), 401


# Home
@FloorIncharge1.route("/")
def home():
    if not session.get('logged_in'):
        return jsonify({'response': 'Not Logged In'})
    else:
        return jsonify({'response': 'Logged In'})

@FloorIncharge1.route("/floorincharge/login", methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        return jsonify({"Error": "Username and Password Not Defined"})

    # Replace the hardcoded password check with a secure authentication mechanism
    if username and password == '123456':
        session['logged_in'] = True
        token = handlers.create_tocken(username='123456', user_id = 123456)
        # handlers.decode_and_verify_token(token)
        return token
        # print("Hello world")
    else:
        return make_response('Unable to Verify', 403, {'www-Authenticate': 'Basic realm: "Authentication Failed!"'})


@FloorIncharge1.route("/generate_token")
def generate_token():
    # Generate the token using your create_token function
    token_response = handlers.create_tocken(username="example_user", user_id=123)

    # Extract the token from the response
    # token = token_response.get_json().get('token')

    # Now you can pass the token to decode_and_verify_token
    # decoded_token = handlers.decode_and_verify_token(token)
    
    # Now you can pass the token to decode_and_verify_token
    expired_token = handlers.is_token_expired(token_response)
    # print(expired_token)

    # Handle the decoded token as needed

    # return "Token generated and decoded successfully!"
    return expired_token

@FloorIncharge1.route("/floorincharge")
def FloorIncharge():
    return "<h1>This is home page</h1>"
