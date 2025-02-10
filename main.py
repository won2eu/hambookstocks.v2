from fastapi import FastAPI
from app.dependencies.db import *
from app.routers import auth_routers

import os
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

create_db_and_table()

app = FastAPI()

# 프론트 연결
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/index")

@app.get("/{page_name}", response_class=HTMLResponse)
async def get_page(page_name: str = "index"):
    page_path = f"frontend/{page_name}.html"
    if os.path.exists(page_path):
        with open(page_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="페이지를 찾을 수 없습니다.", status_code=404)

app.include_router(auth_routers.router)
