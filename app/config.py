import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/unihack')
