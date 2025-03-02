from fastapi import APIRouter
from app.services.crawler_service import mk_crawler
from app.services.GPT_service import summarize_news
from pydantic import BaseModel
from typing import Dict, Any, List

router = APIRouter()


class news_resp(BaseModel):
    message: str
    summarized_news: List[Dict[str, Any]]


@router.get("/news", response_model=news_resp)
def get_news():
    news_json = mk_crawler()
    summarized_news = summarize_news(news_json)

    return news_resp(message="뉴스 업데이트 성공", summarized_news=summarized_news)
