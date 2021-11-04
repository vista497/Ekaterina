from urllib.parse import urlparse
from boto.s3.connection import S3Connection
import os
from dotenv import load_dotenv
import logging

load_dotenv()

#DataBase
url='postgres://hhaqhpjyhtobsz:653c803a5d1a7f1cc86856eb1178c01b6ddbe6d16a31d8f760bad12f295444f5@ec2-52-208-221-89.eu-west-1.compute.amazonaws.com:5432/da2u9nb473rkqt'
result=urlparse(str(url))
USER = result.username
PASS = result.password
DATABASE = result.path[1:]
HOST = result.hostname
PORT = result.port

#ApiKey
#SPEECHKIT=os.environ.get('apiKey_speechKit')
TELEGRAM=os.environ.get('API_TG')
logging.info(TELEGRAM)
#TELEGRAM='2088636244:AAHGkiVJZpvWAKwmtWJ3-KAIhiZ8x90U-2E'
