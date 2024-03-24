from flask import Flask, request, jsonify
import boto3
import os
from Config.creds import BaseConfig

app = Flask(__name__)

# AWS S3 Configuration
# AWS_ACCESS_KEY_ID = "AKIAWABXIQIDMP3BNRKE"
# AWS_ACCESS_KEY_ID = BaseConfig.AWS_S3_ACCESS_KEY
AWS_ACCESS_KEY_ID = "AKIAWABXIQIDMP3BNRKE"
AWS_SECRET_ACCESS_KEY = "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"
S3_BUCKET = 'displayunit'
S3_REGION = 'ap-south-1'

def return_s3_client():
    s3_client = boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    return s3_client

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file:
#         # file_path = os.path.join('uploads', file.filename)
#         s3_client.upload_fileobj(
#             file,
#             S3_BUCKET,
#             file.filename)

#         file_url = f'https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file.filename}'
#         return jsonify({'url': file_url}), 200

# if __name__ == '__main__':
#     app.run(debug=True)

