from fastapi import APIRouter, Depends, HTTPException, Header
from app.dependencies.redis_db import get_redis
from app.dependencies.db import get_db_session
from app.models.DB_user_models import User
from app.models.parameter_models import MyPageResp, ChangePwd
from app.services.mypage_service import AccountService
from app.services.auth_service import AuthService
from sqlmodel import select, update
from app.services.redis_service import RedisService
from app.models.DB_mystocks_models import MyStocks

router = APIRouter(prefix="/mypage")


"""
기본정보 로드
"""


@router.get("/", response_model=MyPageResp)
async def get_mypage(
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    db=Depends(get_db_session),
) -> MyPageResp:
    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, deatil="토큰이 필요합니다.")
    # 토큰 검사

    login_id = await redis_db.get(token)
    print(login_id)
    if not login_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    # login_id 에 해당하는 User 정보 조회
    user = db.exec(select(User).where(User.login_id == login_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return MyPageResp(
        name=user.name, login_id=user.login_id, email=user.email, balance=user.balance
    )


"""
회원탈퇴
"""


@router.post("/delete_account")
async def delete_account(
    authorization: str = Header(None),
    db=Depends(get_db_session),
    redis_db=Depends(get_redis),
    redis_service: RedisService = Depends(),
):
    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="토큰이 필요합니다.")

    login_id = await redis_db.get(token)
    if not login_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    my_stock = db.exec(select(MyStocks).where(MyStocks.login_id == login_id)).first()
    await redis_service.delete_stock(redis_db, my_stock.stock_name)

    service = AccountService(db)
    service.delete_victim_stock(login_id)
    service.delete_account(login_id)
    await redis_db.delete(redis_db, token)  # redis에서 삭제

    return {"message": "User account deleted"}


"""
GG버튼
"""


@router.post("/gg")
async def gg(
    authorization: str = Header(None),
    db=Depends(get_db_session),
    redis_db=Depends(get_redis),
    redis_service: RedisService = Depends(),
):
    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="토큰이 필요합니다.")

    login_id = await redis_db.get(token)
    if not login_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    my_stock = db.exec(select(MyStocks).where(MyStocks.login_id == login_id)).first()
    await redis_service.delete_stock(redis_db, my_stock.stock_name)

    service = AccountService(db)
    # login_id가 상장한 주식을 갖고 있는 사람 주식 모두 삭제

    service.delete_victim_stock(login_id)
    service._delete_user_stocks(login_id)
    service._delete_user_owned_stocks(login_id)  # 본인 보유 주식 삭제
    db.query(User).filter(User.login_id == login_id).update(
        {"balance": 1000000}
    )  # 잔고 다시 업데이트

    db.commit()

    return {"message": "gg"}


"""
비번 변경
"""


@router.post("/change_pwd")
async def change_pwd(
    req: ChangePwd,
    authorization: str = Header(None),
    db=Depends(get_db_session),
    redis_db=Depends(get_redis),
):
    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="토큰이 필요합니다.")

    login_id = await redis_db.get(token)
    if not login_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    print(login_id)
    # 기존 비밀번호 확인
    user = db.exec(select(User).where(User.login_id == login_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    if not AuthService.verify_pwd(req.origin_pwd, user.pwd):
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

    # 입력한 비번 2개 제대로 입력햇는지 검사
    if req.new_pwd != req.check_new_pwd:
        raise HTTPException(status_code=400, detail="새 비밀번호가 일치하지 않습니다.")

    # db에 새로운 해싱된 비밀번호 업데이트
    new_hpwd = AuthService.get_hashed_pwd(req.new_pwd)
    db.exec(update(User).where(User.login_id == login_id).values(pwd=new_hpwd))
    db.commit()

    return {"message": "비밀번호가 성공적으로 변경되었습니다."}


"""
내 주식 상장
"""
