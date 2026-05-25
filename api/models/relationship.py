import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from api.database.base import Base

class EntityRelationship(Base):
    __tablename__ = "entity_relationships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    entity_a = Column(String, index=True, nullable=False)
    relationship_type = Column(String, nullable=False)
    entity_b = Column(String, index=True, nullable=False)
    
    confidence_score = Column(Float, default=0.0)
    source_count = Column(Integer, default=1)
    
    last_seen_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
