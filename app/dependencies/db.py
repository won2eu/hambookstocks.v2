from sqlmodel import(
    SQLModel, Session, create_engine, text)

BLOG_DB_URL = 'sqlite:///blog.db'
MYSTOCKS_DB_URL = 'sqlite:///mystocks.db'

DB_CONN_ARGS = {
    "check_same_thread": False
}

BLOG_DB_ENGINE = create_engine(
    BLOG_DB_URL, connect_args=DB_CONN_ARGS
)

MYSTOCKS_DB_ENGINE = create_engine(
    MYSTOCKS_DB_URL, connect_args=DB_CONN_ARGS
)

def get_blog_db_session():
    with Session(BLOG_DB_ENGINE) as sess:
        yield sess

def get_mystocks_db_session():
    with Session(MYSTOCKS_DB_ENGINE) as sess:
        yield sess

def create_db_and_table():
    SQLModel.metadata.create_all(BLOG_DB_ENGINE)
    SQLModel.metadata.create_all(MYSTOCKS_DB_ENGINE)

def put_temp_data():
    db = MYSTOCKS_DB_ENGINE
    with Session(db) as session:
        session.exec(text("DELETE FROM MyStocks"))
        session.exec(text("INSERT INTO MyStocks (login_id, quantity, stock_code, bought_price) VALUES ('id1', 10, '005930', 80000)"))
        session.exec(text("INSERT INTO MyStocks (login_id, quantity, stock_code, bought_price) VALUES ('jin', 5, '000660', 60000)"))
        session.exec(text("INSERT INTO MyStocks (login_id, quantity, stock_code, bought_price) VALUES ('jin', 7, '005930', 20000)"))

        session.commit()


