from urllib.parse import urlparse
from boto.s3.connection import S3Connection
import os

#DataBase
class Config:
    def __init__(self) -> None:
        
        self.result=urlparse(S3Connection(os.environ['DATABASE_URL']))
        self.USER = self.result.username
        self.PASS = self.result.password
        self.DATABASE = self.result.path[1:]
        self.HOST = self.result.hostname
        self.PORT = self.result.port

        #ApiKey
        self.SPEECHKIT=S3Connection(os.environ['apiKey_speechKit'])
        self.TELEGRAM=S3Connection(os.environ['apiKey_tg'])
