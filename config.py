import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SMS_TOKEN = os.getenv('SMS_TOKEN')
    HOST = '0.0.0.0'
    PORT = '1211'

class Development(Config):
    DEBUG = True
    DEVELOPMENT = True


class Production(Config):
    DEBUG = False
