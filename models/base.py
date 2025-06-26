from datetime import datetime, timezone
from core.db import Base
from sqlalchemy import Column, DateTime


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))
