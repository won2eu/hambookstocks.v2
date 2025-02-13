from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.dependencies.db import *
from app.routers import (trade_routers,auth_routers, record_routers, mystocks_routers, stock_routers, set_page_routers)

import os
from fastapi.staticfiles import StaticFiles

create_db_and_table()

app = FastAPI()

# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (배포 시에는 특정 도메인으로 제한)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 프론트 연결
app.mount("/front/assets", StaticFiles(directory="front/assets"), name="assets")
app.mount("/front/vendor", StaticFiles(directory="front/vendor"), name="vendor")
app.mount("/front2/assets", StaticFiles(directory="front2/assets"), name="assets")


app.include_router(mystocks_routers.router)
app.include_router(auth_routers.router)
app.include_router(record_routers.router)
app.include_router(stock_routers.router)
app.include_router(trade_routers.router)
app.include_router(set_page_routers.router)



# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from app.dependencies.db import *
# from app.routers import auth_routers, record_routers, mystocks_routers, stock_routers
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# import os
# import asyncio
# import random
# import datetime

# # FastAPI 애플리케이션 초기화
# app = FastAPI()

# create_db_and_table()
# put_temp_data()  # 임시 데이터 추가

# # ✅ CORS 설정 추가
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 모든 도메인 허용 (배포 시에는 특정 도메인으로 제한)
#     allow_credentials=True,
#     allow_methods=["*"],  # 모든 HTTP 메서드 허용
#     allow_headers=["*"],  # 모든 헤더 허용
# )

# # ✅ 프론트엔드 파일 제공
# app.mount("/front/assets", StaticFiles(directory="front/assets"), name="assets")
# app.mount("/front/vendor", StaticFiles(directory="front/vendor"), name="vendor")
# app.mount("/front2/assets", StaticFiles(directory="front2/assets"), name="assets")

# # ✅ API 라우터 추가
# app.include_router(mystocks_routers.router)
# app.include_router(auth_routers.router)
# app.include_router(record_routers.router)
# app.include_router(stock_routers.router)

# # ✅ 기본 페이지 라우트
# @app.get("/", response_class=RedirectResponse)
# async def root():
#     return RedirectResponse(url="/front/index")

# @app.get("/front/{page_name}", response_class=HTMLResponse)
# async def get_page(page_name: str = "index"):
#     page_path = f"front/{page_name}.html"
#     if os.path.exists(page_path):
#         with open(page_path, "r", encoding="utf-8") as file:
#             content = file.read()
#         return HTMLResponse(content=content)
#     else:
#         return HTMLResponse(content="페이지를 찾을 수 없습니다.", status_code=404)

# @app.get("/front2/{page_name}", response_class=HTMLResponse)
# async def get_page(page_name: str = "index"):
#     page_path = f"front2/{page_name}.html"
#     if os.path.exists(page_path):
#         with open(page_path, "r", encoding="utf-8") as file:
#             content = file.read()
#         return HTMLResponse(content=content)
#     else:
#         return HTMLResponse(content="페이지를 찾을 수 없습니다.", status_code=404)


# ############################################## ✅ 실시간 모의 테스트 웹소켓 ###################################

# # 테스트할 주식 종목 리스트
# STOCK_CODES = [
#     "005930",  # 삼성전자
#     "000660",  # SK하이닉스
#     "005380",  # 현대자동차
#     "000270",  # 기아
#     "005490",  # POSCO홀딩스
#     "012450",  # 한화에어로스페이스
#     "403870",  # HPSP
#     "042700",  # 한미반도체
#     "086520",  # 에코프로
#     "247540",  # 에코프로비엠
#     "066970",  # 엘앤에프
#     "278280",  # 천보
#     "253590",  # 네오셈
#     "348370",  # 엔켐
#     "028300",  # HLB
#     "196170",  # 알테오젠
#     "092870",  # 엑시콘
#     "000250",  # 삼천당제약
#     "095610",  # 테스
#     "210980"   # SK디앤디
# ]

# # 주식 응답 모델
# class StockPriceResponse(BaseModel):
#     stock_code: str
#     timestamp: str  # HHMMSS 형식
#     current_price: int  # 정수 가격

# # ✅ 웹소켓 핸들러 추가
# @app.websocket("/ws/stocks/1")
# async def websocket_stock_prices(websocket: WebSocket):
#     """클라이언트가 연결되면 1초마다 랜덤 주식 데이터를 보냄 (가끔 데이터 누락 포함)"""
    
#     await websocket.accept()  # 웹소켓 연결 수락

#     try:
#         while True:
#             stock_data_list = []

#             # 랜덤하게 몇 개 데이터를 제외 (최대 9개까지 빠질 수 있음)
#             missing_count = 19 #random.randint(0, 9)
#             selected_stocks = random.sample(STOCK_CODES, len(STOCK_CODES) - missing_count)

#             for stock_code in selected_stocks:
#                 stock_price = 9999  # 5만~20만 원 사이 랜덤 가격
#                 timestamp = datetime.datetime.now().strftime("%H%M%S")  # HHMMSS 형식

#                 stock_response = StockPriceResponse(
#                     stock_code=stock_code,
#                     timestamp=timestamp,
#                     current_price=stock_price,
#                 )
#                 stock_data_list.append(stock_response.dict())

#             # JSON 데이터 전송
#             await websocket.send_json(stock_data_list)
#             await asyncio.sleep(1)  # 1초 단위로 업데이트

#     except WebSocketDisconnect:
#         print("❌ 클라이언트 연결 종료")
