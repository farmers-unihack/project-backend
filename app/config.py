import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/unihack')
    ENV = os.environ.get('ENV', 'development')
    SECRET_KEY = os.environ.get('SECRET_KEY', "supersecretkey")
