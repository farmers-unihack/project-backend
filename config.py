import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # TODO add mongouri here?
    SESSION_TYPE = os.getenv("SESSION_TYPE", "mongodb")
    SESSION_PERMANENT = os.getenv("SESSION_PERMANENT", False)
    SESSION_USE_SIGNER = os.getenv("SESSION_USE_SIGNER", True)
    SESSION_KEY_PREFIX = os.getenv("SESSION_KEY_PREFIX", "farmers-session:")
