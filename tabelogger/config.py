import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

mysql_database_config = {
    "host": os.getenv('MYSQL_HOST'),
    "db": os.getenv('MYSQL_DATABASE_NAME'),
    "user": os.getenv('MYSQL_USER_NAME'),
    "passwd": os.getenv('MYSQL_USER_PASSWORD'),
    "charset": os.getenv('MYSQL_CHARSET'),
}
