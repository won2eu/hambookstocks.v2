from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.parameter_models import *
from app.models.DB_user_models import User
from app.dependencies.db import *
from app.dependencies.redis_db import *
from app.dependencies.jwt_utils import JWTUtil
from app.services.auth_service import AuthService
from app.services.redis_service import RedisService
from app.dependencies.redis_db import get_redis
from typing import Annotated
from sqlmodel import select


router = APIRouter(prefix="/auth")


# 회원가입
@router.post("/register", response_model=AuthResp)
def register(
    req: AuthSignupReq, db=Depends(get_db_session), authService: AuthService = Depends()
):
    existing_user = (
        db.query(User).filter(User.login_id == req.login_id).first()
    )  # 아이디 중복체크
    if existing_user:
        raise HTTPException(status_code=400, detail="ID already exists")

    # 이미 존재하는 이메일인지 확인하는 것
    existing_email = db.exec(select(User).where(User.email == req.email)).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="E-mail already exists")

    new_user = authService.signup(db, req.login_id, req.pwd, req.name, req.email)

    if not new_user:
        raise HTTPException(status_code=400, detail="Failed to register")

    return AuthResp(message="User registered successfully", user=new_user)


# 로그인
@router.post("/login")
async def login(
    req: AuthSigninReq,
    db=Depends(get_db_session),
    jwtUtil: JWTUtil = Depends(),
    authService: AuthService = Depends(),
    redis_db=Depends(get_redis),
    redisService: RedisService = Depends(),
):

    user = authService.signin(db, req.login_id, req.pwd)
    if not user:
        raise HTTPException(status_code=401, detail="Login failed")

    access_token = jwtUtil.create_token(user.model_dump())
    # redis 에 토큰넣기
    await redisService.add_token(redis_db, access_token, req.login_id)

    return AuthResp(
        message="로그인 되었습니다.",
        user=user,
        access_token=access_token,  # front에 토큰을 응답으로 반환
    )


# 로그아웃
@router.post("/logout")
async def auth_logout(
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    redisService: RedisService = Depends(),
):  # 헤더에서 토큰을 받음
    if not authorization:
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")

    token = authorization.split(" ")[1]  # "Bearer <토큰>"에서 토큰만 추출

    if not await redis_db.get(token):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    await redisService.delete_token(redis_db, token)

    return {"message": "로그아웃 되었습니다."}


@router.post("/check-token")
def check_token(Authorization: Annotated[str, Header()], jwtUtil: JWTUtil = Depends()):
    token = Authorization.replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")
    try:
        payload = jwtUtil.decode_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token decode error")

    login_id = payload.get("login_id")

    if login_id is None:
        raise HTTPException(status_code=400, detail="Login ID not found in token")
    return {"message": "Token is valid"}
