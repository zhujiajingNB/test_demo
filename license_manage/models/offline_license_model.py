from sqlalchemy import Column, String, SMALLINT, BIGINT, DateTime, Boolean
from datetime import datetime
from database import Base, engine

# 指纹数据库映射表
class OfflineLicense(Base):
    __tablename__ = 'offline_license'

    id = Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    offline_version = Column(String(50))
    path = Column(String(100))
    is_delete = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now())
    comment = Column(String(100))

if __name__ == '__main__':
    Base.metadata.create_all(engine)