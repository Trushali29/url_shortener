from sqlalchemy import Boolean, Column, Integer, String, DateTime
from .database import Base
from  datetime import datetime
class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    key=Column(String, unique=True, index=True, nullable=False)
    secret_key = Column(String, unique=True, index=True, nullable=False)
    target_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    delete_at = Column(DateTime, nullable=True)


