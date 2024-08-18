from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    role: str  # 사용자 역할 (student, parent, teacher, admin)
    grade: Optional[int] = None
    classroom: Optional[int] = None
    number: Optional[int] = None
