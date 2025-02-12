from sqlmodel import(
    SQLModel, Session, create_engine, text)

DB_URL = 'sqlite:///db.db'

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

def put_temp_data():
    db = DB_ENGINE
    with Session(db) as session:
        session.exec(text("DELETE FROM MyStocks"))
        session.exec(text("INSERT INTO MyStocks (login_id, quantity, stock_code, bought_price) VALUES ('id1', 10, '005930', 80000)"))
        session.exec(text("INSERT INTO MyStocks (login_id, quantity, stock_code, bought_price) VALUES ('jin', 5, '000660', 60000)"))
        session.exec(text("INSERT INTO MyStocks (login_id, quantity, stock_code, bought_price) VALUES ('jin', 7, '005930', 20000)"))

        session.commit()


