import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.environ.get('client-id', None)
CLIENT_SECRET = os.environ.get('client-secret', None)
GPT_API_KEY= os.environ.get('gptKey', None)
DOMAIN_NAME= os.environ.get('domain-name', None)