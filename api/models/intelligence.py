import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from api.database.base import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    source = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    summary = Column(String)
    sentiment = Column(String) # positive, neutral, negative
    credibility_score = Column(Integer)
    tags = Column(ARRAY(String), default=list)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class WebsiteReport(Base):
    __tablename__ = "website_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    domain = Column(String, unique=True, index=True, nullable=False)
    technologies = Column(ARRAY(String), default=list)
    seo_score = Column(Integer)
    performance_score = Column(Integer)
    security_status = Column(String) # secure, warning, critical
    social_links_count = Column(Integer, default=0)
    last_scanned_at = Column(DateTime, default=datetime.utcnow)

class TrendingTopic(Base):
    __tablename__ = "trending_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    topic = Column(String, unique=True, index=True, nullable=False)
    category = Column(String)
    trend_direction = Column(String) # up, down, flat
    activity_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
