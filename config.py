from urllib.parse import urlparse
from boto.s3.connection import S3Connection
import os

#DataBase
result=urlparse(os.environ['DATABASE_URL'])
USER = result.username
PASS = result.password
DATABASE = result.path[1:]
HOST = result.hostname
PORT = result.port

#ApiKey
SPEECHKIT=os.environ['apiKey_speechKit']
TELEGRAM=os.environ['apiKey_tg']
