import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from api.database.base import Base

class EntitySnapshot(Base):
    __tablename__ = "entity_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    entity_name = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    
    mention_count = Column(Integer, default=0)
    source_diversity = Column(Integer, default=0)
    
    github_stars = Column(Integer, default=0)
    github_star_velocity = Column(Integer, default=0)
    
    reddit_discussion_intensity = Column(Integer, default=0)
    sentiment_score = Column(Float, default=0.0)
    
    velocity_score = Column(Integer, default=0)
    lifecycle_state = Column(String)
