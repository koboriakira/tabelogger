import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

mysql = {
    "host": os.getenv('MYSQL_HOST'),
    "db": os.getenv('MYSQL_DATABASE_NAME'),
    "user": os.getenv('MYSQL_USER_NAME'),
    "passwd": os.getenv('MYSQL_USER_PASSWORD'),
    "charset": os.getenv('MYSQL_CHARSET'),
}


def pymysql_session() -> Session:
    DATABASE = f'mysql+pymysql://{mysql["user"]}:{mysql["passwd"]}@{mysql["host"]}/{mysql["db"]}?charset=utf8'
    engine = create_engine(
        DATABASE,
        encoding="utf-8",
        echo=True  # Trueだと実行のたびにSQLが出力される
    )
    SqlAlchemySession = sessionmaker(bind=engine)
    return SqlAlchemySession()
