from sqlmodel import(
    SQLModel, Session, create_engine)

BLOG_DB_URL = 'sqlite:///blog.db'
TRADE_DB_URL = 'sqlite:///trade.db'

DB_CONN_ARGS = {
    "check_same_thread": False
}

BLOG_DB_ENGINE = create_engine(
    BLOG_DB_URL, connect_args=DB_CONN_ARGS
)

TRADE_DB_ENGINE = create_engine(
    TRADE_DB_URL, connect_args=DB_CONN_ARGS
)

def get_blog_db_session():
    with Session(BLOG_DB_ENGINE) as sess:
        yield sess

def get_trade_db_session():
    with Session(TRADE_DB_ENGINE) as sess:
        yield sess

def create_db_and_table():
    SQLModel.metadata.create_all(BLOG_DB_ENGINE)
    SQLModel.metadata.create_all(TRADE_DB_ENGINE)
