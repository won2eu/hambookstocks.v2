from fastapi.middleware.cors import CORSMiddleware  # CORS, MIDDLE WARE 조필1
from fastapi import FastAPI  # FAST API IMPORT
from app.dependencies.db import *
from app.routers import (
    trade_routers,
    auth_routers,
    record_routers,
    mystocks_routers,
    stock_routers,
    set_page_routers,
    get_news_routers,
    make_stock_routers,
    mypage_routers,
)

from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.trade_service import clear_trend


create_db_and_table()

app = FastAPI()
scheduler = BackgroundScheduler()


app.add_middleware(  # CORS MIDDLE WARE
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/front/assets", StaticFiles(directory="front/assets"), name="assets")
app.mount("/front/vendor", StaticFiles(directory="front/vendor"), name="vendor")
app.mount("/front2/assets", StaticFiles(directory="front2/assets"), name="assets")


app.include_router(mystocks_routers.router)  # ROUTER 연결
app.include_router(auth_routers.router)
app.include_router(record_routers.router)
app.include_router(stock_routers.router)
app.include_router(trade_routers.router)
app.include_router(set_page_routers.router)
app.include_router(get_news_routers.router)
app.include_router(make_stock_routers.router)
app.include_router(mypage_routers.router)

scheduler.add_job(clear_trend, "interval", minutes=60)
scheduler.start()
