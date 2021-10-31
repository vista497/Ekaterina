from urllib.parse import urlparse
from boto.s3.connection import S3Connection
import os

#DataBase
url=os.environ.get('DATABASE_URL')
#url=S3Connection(os.environ[DATABASE_URL])
result=urlparse(str(url))
USER = result.username
PASS = result.password
DATABASE = result.path[1:]
HOST = result.hostname
PORT = result.port

#ApiKey
SPEECHKIT=os.environ.get('apiKey_speechKit')
TELEGRAM=os.environ.get('apiKey_tg')
