from pydantic import BaseModel, EmailStr
from typing import Optional

# 기본적인 User 스키마
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str

# 회원가입 시 사용할 스키마
class UserCreate(UserBase):
    password: str
    grade: Optional[int] = None  # 학년 (학생 및 학부모)
    classroom: Optional[int] = None  # 반 (학생 및 학부모)
    number: Optional[int] = None  # 번호 (학생 및 학부모)

# 응답으로 사용할 User 스키마 (비밀번호 제외)
class UserResponse(UserBase):
    id: int
    grade: Optional[int] = None  # 학년
    classroom: Optional[int] = None  # 반
    number: Optional[int] = None  # 번호

    class Config:
        from_attributes = True

# 로그인 시 사용할 스키마
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
