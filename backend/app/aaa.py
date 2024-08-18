from sqlmodel import Session, select, create_engine
from models import User  # 모델을 정의한 파일

# 데이터베이스 연결 설정
engine = create_engine("sqlite:///./app.db")

# 세션을 통해 데이터 조회
with Session(engine) as session:
    admin_user = session.exec(select(User).where(User.username == "admin")).first()
    if admin_user:
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print(f"Hashed Password: {admin_user.hashed_password}")
        print(f"Role: {admin_user.role}")
    else:
        print("Admin user not found")
