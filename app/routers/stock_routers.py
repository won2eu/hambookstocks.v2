import websockets
import json
import requests
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
import os

load_dotenv()

g_appkey = os.getenv("APP_KEY")
g_appsecret = os.getenv("APP_SECRET")


router = APIRouter()

STOCK_CODES = [
    "005930", "000660", "005380", "000270", "005490",
    "012450", "403870", "042700", "086520", "247540",
    "066970", "278280", "253590", "348370", "028300",
    "196170", "272210", "000250", "095610", "210980"
]


def get_approval(key, secret):
    url = 'https://openapi.koreainvestment.com:9443/oauth2/Approval'
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials", "appkey": key, "secretkey": secret}
    res = requests.post(url, headers=headers, data=json.dumps(body))
    return res.json()["approval_key"]


def parse_stock_data(data):
    """실시간 주식 데이터를 파싱하는 함수"""
    pValue = data.split('^')
    stock_code = pValue[0]
    stock_time = pValue[1]
    stock_price = pValue[2]
    return stock_code, stock_time, stock_price


@router.websocket("/ws/stocks")
async def websocket_stock_prices(websocket: WebSocket):
    """모든 종목의 실시간 데이터를 리스트로 프론트엔드에 전송"""
    await websocket.accept()

    approval_key = get_approval(g_appkey, g_appsecret)
    url = 'ws://ops.koreainvestment.com:21000'
    custtype = 'P'
    tr_id = 'H0STCNT0'
    tr_type = '1'

    try:
        async with websockets.connect(url, ping_interval=60, ping_timeout=20) as upstream_ws:
            # 모든 종목 구독 등록
            for code in STOCK_CODES:
                senddata = json.dumps({
                    "header": {
                        "approval_key": approval_key,
                        "custtype": custtype,
                        "tr_type": tr_type,
                        "content-type": "utf-8"
                    },
                    "body": {
                        "input": {
                            "tr_id": tr_id,
                            "tr_key": code
                        }
                    }
                })
                await upstream_ws.send(senddata)
                await asyncio.sleep(0.2)

            while True:
                stock_data_list = []  # 모든 주식 데이터를 저장할 리스트
                
                for _ in range(len(STOCK_CODES)):  # 모든 종목에 대해 데이터를 받음
                    data = await upstream_ws.recv()

                    if data.startswith('0'):  # 실시간 체결 데이터
                        recvstr = data.split('|')
                        if recvstr[1] == tr_id:
                            data_cnt = int(recvstr[2])
                            stock_data = recvstr[3]
                            stock_code, stock_time, stock_price = parse_stock_data(stock_data)

                            stock_info = {
                                "stock_code": stock_code,
                                "timestamp": stock_time,
                                "current_price": stock_price
                            }

                            stock_data_list.append(stock_info)  # 리스트에 추가

                if stock_data_list:
                    await websocket.send_json(stock_data_list)  # 리스트로 변환하여 JSON 전송
                    #print(f"📡 전송된 데이터: {stock_data_list}")

                await asyncio.sleep(2)  # 2초 간격으로 업데이트

    except WebSocketDisconnect:
        print("❌ 클라이언트와의 WebSocket 연결 종료")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"웹소켓 연결 종료: {e}")