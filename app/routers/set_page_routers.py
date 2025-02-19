from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
import os  # 조필12

# 프론트 관련은 여기에..
router = APIRouter()


@router.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/front/index")


@router.get("/front/{page_name}", response_class=HTMLResponse)
async def get_page(page_name: str = "index"):
    page_path = f"front/{page_name}.html"
    if os.path.exists(page_path):
        with open(page_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="페이지를 찾을 수 없습니다.", status_code=404)


@router.get("/front2/{page_name}", response_class=HTMLResponse)
async def get_page(page_name: str = "index"):
    page_path = f"front2/{page_name}.html"
    if os.path.exists(page_path):
        with open(page_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="페이지를 찾을 수 없습니다.", status_code=404)
