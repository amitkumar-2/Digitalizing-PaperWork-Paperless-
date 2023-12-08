from flask import Blueprint, render_template, request, session, jsonify, make_response
import handlers

FloorIncharge1=Blueprint('FloorIncharge', __name__)


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
        token = handlers.create_tocken(username=username)
        handlers.decode_and_verify_token(token)
        return token
        # print("Hello world")
    else:
        return make_response('Unable to Verify', 403, {'www-Authenticate': 'Basic realm: "Authentication Failed!"'})


@FloorIncharge1.route("/generate_token")
def generate_token():
    # Generate the token using your create_token function
    token_response = handlers.create_tocken("example_user")

    # Extract the token from the response
    token = token_response.get_json().get('token')

    # Now you can pass the token to decode_and_verify_token
    decoded_token = handlers.decode_and_verify_token(token)
    
    # Now you can pass the token to decode_and_verify_token
    # expired_token = handlers.is_token_expired(token)

    # Handle the decoded token as needed

    return "Token generated and decoded successfully!"

@FloorIncharge1.route("/floorincharge")
def FloorIncharge():
    return "<h1>This is home page</h1>"
