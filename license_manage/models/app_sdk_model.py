from sqlalchemy import Column, String, BIGINT, DateTime, Boolean, func
from datetime import datetime
from database import Base, engine

# 指纹数据库映射表
class AppSdk(Base):
    __tablename__ = 'app_sdk'

    id = Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    sdk_name = Column(String(50))
    sdk_version = Column(String(20))
    path = Column(String(100))
    is_delete = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime,server_default=func.now() ,onupdate=func.now())
    comment = Column(String(100))

if __name__ == '__main__':
    Base.metadata.create_all(engine)