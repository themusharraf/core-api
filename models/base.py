from datetime import datetime
from core.db import Base
from sqlalchemy import Column, DateTime


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
