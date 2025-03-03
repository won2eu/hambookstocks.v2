from sqlmodel import SQLModel, Field
import re
from pydantic import field_validator


class User(SQLModel, table=True):
    __tablename__ = "Users"

    id: int | None = Field(default=None, primary_key=True)
    login_id: str = Field(index=True)
    pwd: str = Field(exclude=True)
    name: str
    balance: float = Field(default=0.0)
    email: str

    # 비밀번호 정규표현식 검증 (8~20자, 숫자 + 영어 필수)
    @field_validator("pwd")
    @classmethod
    def validate_password(cls, value):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$"
        if not re.match(pattern, value):
            raise ValueError("비밀번호는 8~20자이며, 숫자와 영어를 포함해야 합니다.")
        return value

    # 이메일 정규표현식 검증 (@ 포함, .com 또는 .net)
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.(com|net)$"
        if not re.match(pattern, value):
            raise ValueError("유효하지 않은 email 형식 입니다.")
        return value
