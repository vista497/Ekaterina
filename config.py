from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

#DataBase
url=os.environ.get('DATABASE_URL')
result=urlparse(url)
USER = result.username
PASS = result.password
DATABASE = result.path[1:]
HOST = result.hostname
PORT = result.port

#ApiKey
#SPEECHKIT=os.environ.get('apiKey_speechKit')
TELEGRAM=os.environ.get('API_TG')

