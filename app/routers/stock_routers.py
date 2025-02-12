from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import websockets  # 한국투자증권 API WebSocket 연결을 위해 필요
from app.services.stock_service import stockspurchase, get_approval
from app.models.stock_model import StockPriceResponse
import os
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")

router = APIRouter()

# 10개 종목 리스트
STOCK_CODES = [
    "005930",  # 삼성전자
    "000660",  # SK하이닉스
    "373220",  # LG에너지솔루션
    "207940",  # 삼성바이오로직스
    "005380",  # 현대차
    "035420",  # NAVER
    "035720",  # 카카오
    "068270",  # 셀트리온
    "000270",  # 기아
    "105560"   # KB금융
]



@router.websocket("/ws/stocks")
async def websocket_stock_prices(websocket: WebSocket):
    """30개 종목의 실시간 가격을 WebSocket을 통해 전송"""
    
    await websocket.accept()  # WebSocket 연결 수락

    try:
        async with websockets.connect("ws://ops.koreainvestment.com:21000", ping_interval=60) as websocket_connection:
            g_approval_key = get_approval(
                APP_KEY,
                APP_SECRET
            )  # API 인증키 발급
            tr_id = "H0STCNT0"
            
            for stock_code in STOCK_CODES:
                senddata = f'''{{
                    "header": {{"approval_key": "{g_approval_key}", "custtype": "P", "tr_type": "1", "content-type": "utf-8"}},
                    "body": {{"input": {{"tr_id": "{tr_id}", "tr_key": "{stock_code}"}}}}
                }}'''
                await websocket_connection.send(senddata)  # 한국투자증권 API에 종목 데이터 요청
            
            while True:
                stock_data_list = []
                
                for stock_code in STOCK_CODES:
                    data = await websocket_connection.recv()  # 실시간 데이터 수신
                    
                    if data[0] == "0":  # 실시간 체결 데이터
                        recvstr = data.split("|")
                        trid0 = recvstr[1]

                        if trid0 == "H0STCNT0":  # 체결 데이터 처리
                            data_cnt = int(recvstr[2])
                            processed_data = stockspurchase(data_cnt, recvstr[3])  # 데이터 가공

                            if processed_data:
                                stock_response = StockPriceResponse(
                                    stock_code=stock_code,
                                    timestamp=processed_data["stock_time"],
                                    current_price=processed_data["stock_price"],
                                )
                                stock_data_list.append(stock_response.model_dump())
                
                await websocket.send_json(stock_data_list)  # JSON 데이터 전송
                await asyncio.sleep(1)  # 1초 간격으로 업데이트

    except WebSocketDisconnect:
        print("❌ WebSocket 연결 종료")
