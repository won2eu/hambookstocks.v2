from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.dependencies.db import *
from app.routers import auth_routers, record_routers, mystocks_routers
#, stock_routers

import os
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

create_db_and_table()

put_temp_data() # 임시 데이터 추가 - 나중에 삭제

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
app.mount("/assets", StaticFiles(directory="front/assets"), name="assets")
app.mount("/vendor", StaticFiles(directory="front/vendor"), name="vendor")

app.include_router(mystocks_routers.router)
app.include_router(auth_routers.router)
app.include_router(record_routers.router)
#app.include_router(stock_routers.router)

@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/index")

@app.get("/{page_name}", response_class=HTMLResponse)
async def get_page(page_name: str = "index"):
    page_path = f"front/{page_name}.html"
    if os.path.exists(page_path):
        with open(page_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="페이지를 찾을 수 없습니다.", status_code=404)

