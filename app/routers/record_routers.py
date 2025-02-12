from fastapi import APIRouter, Depends, HTTPException
from app.models.parameter_models import *
from app.models.user_models import User 
from app.dependencies.db import get_db_session 
from sqlmodel import select, desc

router = APIRouter(
)

### 임시로 돈 주기
@router.post('/record')
def plus_balance(login_id: str, money: float, db=Depends(get_db_session)):
    user = db.exec(select(User).where(User.login_id == login_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # balance 업데이트
    user.balance += money 
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Balance updated successfully", "user_id": user.id, "new_balance": user.balance}
    

# 명예의 전당
@router.get('/record')
def record(limit: int=5, db=Depends(get_db_session)): 
    users = db.exec(
        select(User).order_by(desc(User.balance)).limit(limit)  
    ).all()

    if not users:
        raise HTTPException(status_code=404, detail="Not Found")
    rankings = [
        {"rank": idx + 1, "user_id": user.id, "login_id": user.login_id, "balance": user.balance}
        for idx, user in enumerate(users)
    ]

    return {"message": "조회 성공", "rankings": rankings}
