import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/unihack')
    ENV = os.environ.get('ENV', 'development')
    SECRET_KEY = os.environ.get('SECRET_KEY', "supersecretkey")
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT', False)
    SESSION_USE_SIGNER = os.environ.get('SESSION_USE_SIGNER', True)

