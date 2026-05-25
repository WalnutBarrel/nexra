import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from api.database.base import Base

class ScrapeLog(Base):
    __tablename__ = "scrape_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    source = Column(String, index=True)
    status = Column(String) # success, failed
    items_scraped = Column(Integer, default=0)
    error_message = Column(String, nullable=True)
    duration_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    endpoint = Column(String, index=True)
    method = Column(String)
    status_code = Column(Integer)
    response_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class AdminSetting(Base):
    __tablename__ = "admin_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
