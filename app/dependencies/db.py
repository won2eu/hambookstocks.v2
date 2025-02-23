from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv(override=True)
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
DBNAME = os.environ.get("DBNAME")


DB_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

DB_ENGINE = create_engine(DB_URL, echo=True)


def get_db_session():
    with Session(DB_ENGINE) as sess:
        yield sess


def create_db_and_table():
    SQLModel.metadata.create_all(DB_ENGINE)
