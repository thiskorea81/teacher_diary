from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, SQLModel, create_engine
from contextlib import asynccontextmanager
from .models import User
from .auth import verify_password, get_password_hash, create_access_token
from .database import create_db_and_tables, get_db, engine
from .schemas import UserCreate, UserResponse
import os

# CORS 설정
origins = [
    "http://localhost:5173",  # 허용할 출처 (프론트엔드 개발 서버)
    # 필요에 따라 다른 출처 추가 가능
]

# 데이터베이스 테이블 생성 함수
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 데이터베이스 테이블 생성 및 관리자 계정 초기화
    create_db_and_tables()
    
    # 데이터베이스 연결을 통해 세션을 생성하고 관리자 계정 확인
    with Session(engine) as session:
        # 'admin' 사용자 검색
        admin_user = session.exec(select(User).where(User.username == "admin")).first()
        if not admin_user:
            # 관리자가 없으면 생성
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin"),
                role="admin"
            )
            session.add(admin_user)
            session.commit()
            session.refresh(admin_user)
    
    yield  # 앱이 실행되는 동안 유지

    # Shutdown: 필요 시 정리 작업을 여기에 추가할 수 있습니다.

app = FastAPI(lifespan=lifespan)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # CORS에서 허용할 출처 설정
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if user.role == "student":
        if not (user.grade and user.classroom and user.number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student must provide grade, classroom, and number."
            )
    elif user.role == "parent":
        if not (user.grade and user.classroom and user.number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent must provide student's grade, classroom, and number."
            )

        student = db.exec(select(User).where(
            User.role == "student",
            User.grade == user.grade,
            User.classroom == user.classroom,
            User.number == user.number
        )).first()

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found with the provided grade, classroom, and number."
            )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        grade=user.grade,
        classroom=user.classroom,
        number=user.number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # print(f"Provided password: {form_data.password}")
    # print(f"Stored hash: {user.hashed_password}")

    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "grade": user.grade,
        "classroom": user.classroom,
        "number": user.number,
    }

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.exec(User).all()
    return users

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.hashed_password = get_password_hash(user.password)
    db_user.role = user.role
    db_user.grade = user.grade
    db_user.classroom = user.classroom
    db_user.number = user.number

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# 데이터베이스 설정
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)

# 데이터베이스 재설정 엔드포인트 (임시)
@app.post("/reset-database")
async def reset_database():
    if os.path.exists("database.db"):
        os.remove("database.db")
    SQLModel.metadata.create_all(engine)
    return {"message": "Database reset successful"}