from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.environ.get("MYSQL_USERNAME")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
HOST = os.environ.get("MYSQL_HOST")
PORT = os.environ.get("MYSQL_PORT")
DBNAME = os.environ.get("MYSQL_DBNAME")


DB_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

DB_ENGINE = create_engine(DB_URL, echo=True)


def get_db_session():
    with Session(DB_ENGINE) as sess:
        yield sess


def create_db_and_table():
    SQLModel.metadata.create_all(DB_ENGINE)
