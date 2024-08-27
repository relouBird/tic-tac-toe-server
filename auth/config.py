import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID', None)
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', None)
GPT_API_KEY= os.environ.get('GPT_API_KEY', None)
PORT= int(os.environ.get('PORT', 5000))