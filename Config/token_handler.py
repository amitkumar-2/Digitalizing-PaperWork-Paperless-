from flask import jsonify, request
from functools import wraps
import jwt
from datetime import datetime, timedelta
from pytz import timezone


class TokenRequirements:
    @staticmethod
    def create_token(employee_id, mobile_no, secret_key):
        payload = {
            'mobile_no': mobile_no,
            'employee_id': employee_id,
            'exp': datetime.utcnow() + timedelta(minutes=2),
        }
        return jwt.encode(payload, secret_key, algorithm='HS512')

    @staticmethod
    def decode_and_verify_token(token, secret_key):
        try:
            if isinstance(token, str):
                token = token.encode('utf-8')
            return jwt.decode(token, secret_key, algorithms=['HS512'])
        except jwt.ExpiredSignatureError as e:
            print("Token has expired:", e)
            return None
        except jwt.DecodeError as e:
            print("Error decoding token:", e)
            return None

    @staticmethod
    def is_token_expired(token, secret_key):
        decoded_token = TokenRequirements.decode_and_verify_token(token, secret_key)
        if decoded_token:
            expiration_time = datetime.utcfromtimestamp(decoded_token['exp'])
            current_utc_time = datetime.utcnow()
            return expiration_time <= current_utc_time, decoded_token
        return True, None

    @classmethod
    def token_required(cls, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
            # token = request.args.get('token')
            secret_key = 'nie83jdie98239A9J3H4hdncHSJD8473'  # You should get this from your app config
            if not token:
                return jsonify({'Alert!': 'Token is missing!'}), 401
            token_expired, payload = cls.is_token_expired(token, secret_key)
            if token_expired:
                return jsonify({'Alert!': 'Token is expired or invalid!'}), 401
            kwargs['token_payload'] = payload
            return func(*args, **kwargs)
        return decorated