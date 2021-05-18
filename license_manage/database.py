from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from main_settings import DATABASE_NAME, DATABASE_URL, DATABASE_PASSWORD, DATABASE_USER

# sqlalchemy 连接
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URL}/{DATABASE_NAME}"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@120.77.242.65:3306/fasapi"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    encoding='utf-8',
    echo=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)
#创建基本的映射类
Base = declarative_base(bind=engine, name='base')

# 获取数据库连接s
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

