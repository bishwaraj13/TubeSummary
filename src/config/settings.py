import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR: str = os.getenv("BASE_DIR")
MEDIA_DIR: str = os.getenv("MEDIA_DIR")
