import os
from dotenv import load_dotenv


load_dotenv()

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)
FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID',None)
FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET',None)
PORT= int(os.environ.get('PORT', 5100))
GPT_API_KEY= os.environ.get('GPT_API_KEY', None)
URL_DATABASE= os.environ.get('URL_DATABASE','postgresql://postgres:admin@localhost:5432/postgres')
BACKEND_URL = os.environ.get('BACKEND_URL', None)
FRONTEND_URL= os.environ.get('FRONTEND_URL2','relou.app')