class BaseConfig():
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = False
    MQ_EXCHANGE = 'amq.topic'
    DEFAULT_DEVICE_NAME = "888888888888888"
    FCM_SERVER_KEY = "AAAA2RAsLv0:APA91bFKC-QUxK8atUCvqeFAiMfS9RbQotVjNplqZxtreg873Q2FHRxzjOupwbJpNrbIf4g__ycEUY3h3C0H7jE2ILVuAUUHx7WKvEs0ALSUkL00U57eAPDaZxDwdvdm--eQPYe9_MD6"
    AWS_SNS_ACCES_KEY = "AKIAWABXIQIDOGW5NT2L"
    AWS_SNS_SECRET_KEY = "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"
    AWS_SNS_REGION = "Global"
    AWS_S3_ACCESS_KEY = "AKIAWABXIQIDMP3BNRKE"
    AWS_S3_SECRET_KEY = "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"
    AWS_S3_BUCKET = 'displayunit'
    AWS_S3_REGION = 'ap-south-1'


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    FLASKENV = 'development'
    MQ_URL = 'amqp://pika:start1234@54.65.98.165:5672'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_password@18.212.243.182/my-sql'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://interface:interface@13.201.8.162/DuDB'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://amit:amit@192.168.1.14/DU_APP'
    POSTGRES_SECRET_KEY = 'KOKE92jdwdm(@#Jdkmkcm93)eeijdijioHOUIHDUENJNEOINDIWIONDKWOIDNIOENDIOJIODNNCUIBYRGYVBRVTRBNOXE'
    CELERY_BROKER = 'pyamqp://rabbit_user:rabbit_password@54.65.98.165:5672'
    CELERY_RESULT_BACKEND = 'rpc://rabbit_user:rabbit_password@54.65.98.165:5672'