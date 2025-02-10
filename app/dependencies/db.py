from sqlmodel import(
    SQLModel, Session, create_engine)

DB_URL = 'sqlite:///user.db'
DB_CONN_ARGS = {
    "check_same_thread": False
}

DB_ENGINE = create_engine(
    DB_URL, connect_args=DB_CONN_ARGS
)

def get_db_session():
    with Session(DB_ENGINE) as sess:
        yield sess

def create_db_and_table():
    SQLModel.metadata.create_all(DB_ENGINE)
