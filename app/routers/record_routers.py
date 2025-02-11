from fastapi import APIRouter, Depends, HTTPException
from app.models.parameter_models import *
from app.models.record_model import Record
from app.dependencies.db import *
from sqlmodel import select, desc

router = APIRouter(
    prefix='/auth'
)

# @router.post('/postRecord')
# def post_record(record: Record,db= Depends(get_record_db_session)):
#     recordModel = Record()
#     recordModel.id = record.id
#     recordModel.login_id = record.login_id
#     recordModel.profit_rate = record.profit_rate

#     db.add(recordModel)
#     db.commit()
#     db.refresh(recordModel)
#     return{
#         'result': True
#     }
    
# 명예의 전당
@router.get('/record', response_model=RecordResp)
def record(limit: int=5, db=Depends(get_record_db_session)):
    records = db.exec(
        select(Record).order_by(desc(Record.profit_rate)).limit(limit)
    ).all()
    if not records:
        raise HTTPException(status_code=404, detail="Not Found")
    return RecordResp(message = "조회 성공",
                      records = records
    )


# to do: 결과값 DB에 저장