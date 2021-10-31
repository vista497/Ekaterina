from urllib.parse import urlparse
import os

#DataBase
result=urlparse(os.environ.set('DATABASE_URL'))
USER = result.username
PASS = result.password
DATABASE = result.path[1:]
HOST = result.hostname
PORT = result.port

#ApiKey
SPEECHKIT=os.environ.set('apiKey_speechKit')
TELEGRAM=os.environ.set('apiKey_tg')
