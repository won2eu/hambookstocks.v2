from fastapi import APIRouter, Depends, HTTPException
from app.models.parameter_models import *
from app.models.mystocks_models import MyStocks
from app.dependencies.db import get_mystocks_db_session
from sqlmodel import select

router = APIRouter()

@router.get('/mystocks')
def get_mystocks(login_id: str, db=Depends(get_mystocks_db_session)):
    mystocks = db.exec(select(MyStocks).where(MyStocks.login_id == login_id)).all()
    return {"message": "Mystocks found", "mystocks": mystocks}