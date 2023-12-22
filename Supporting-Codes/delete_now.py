# import jwt
# from datetime import datetime, timedelta

# # Secret key for encoding and decoding the JWT token
# SECRET_KEY = 'your_secret_key'

# # Example data to be encoded in the token
# payload = {
#     'user_id': 123,
#     'username': 'example_user',
#     'exp': datetime.utcnow() + timedelta(seconds=120)  # Expiration time 120 seconds in the future
# }

# # Encode the JWT token
# encoded_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# print("Encoded Token:", encoded_token)

# # Decode and verify the JWT token
# try:
#     decoded_token = jwt.decode(encoded_token, SECRET_KEY, algorithms=['HS256'])
#     print("Decoded Token:", decoded_token)
# except jwt.ExpiredSignatureError as e:
#     print("Token has expired:", e)
# except jwt.DecodeError as e:
#     print("Error decoding token:", e)







import jwt
from datetime import datetime, timedelta
import time

SECRET_KEY = 'your_secret_keynxcwionfoeuiwouh@&#*(@&!_jnjind_----jcdnijw-00329jdnuenf3894njekdncf9384nfjndfc9384fndjcv98o34inf9ec8j438idm4398j)'
SECRET_KEY1 = 'your_secret_keynxcwionfoeuiwouh@&#*(@&!_jnjind_----jcdnijw-00329jdnuenf3894njekdncf9384nfjndfc9384fndjcv98o34inf9ec8j438idm4398j)'

def encode_token(payload):
    # Encode the JWT token
    return jwt.encode(payload, SECRET_KEY, algorithm='HS512')

def decode_and_verify_token(token):
    try:
        # If the token is a string, convert it to bytes before decoding
        if isinstance(token, str):
            token = token.encode('utf-8')
        decoded_token = jwt.decode(token, SECRET_KEY1, algorithms=['HS512'])
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
        return expiration_time <= current_utc_time, decoded_token
    return True

# Example usage
payload = {
    'user_id': 123,
    'username': 'example_user',
    'exp': datetime.utcnow() + timedelta(seconds=11),
    'iat': datetime.utcnow(),
    'nbf': datetime.utcnow(),
    'jti': '1234567890',
    'role': 'admin',
    'iss': 'example_issuer'
}

encoded_token = encode_token(payload)
print("Encoded Token:", encoded_token)

time.sleep(1)

token_payload = is_token_expired(encoded_token)
print(type(token_payload[1]))

# Check if the token has expired
if is_token_expired(encoded_token):
    print("The token has expired.")
else:
    print("The token is still valid.")
