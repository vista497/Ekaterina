from urllib.parse import urlparse
from boto.s3.connection import S3Connection
import os

#DataBase
url=S3Connection(os.environ["DATABASE_URL"])
result=urlparse(url)
USER = result.username
PASS = result.password
DATABASE = result.path[1:]
HOST = result.hostname
PORT = result.port

#ApiKey
SPEECHKIT=S3Connection(os.environ["apiKey_speechKit"])
TELEGRAM=S3Connection(os.environ["apiKey_tg"])
