from dotenv import load_dotenv
import os

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')
SERVER_CODE = os.getenv('SERVER_CODE')
