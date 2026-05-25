import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from api.database.base import Base

class Collection(Base):
    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SavedDossier(Base):
    __tablename__ = "saved_dossiers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("collections.id"), nullable=False)
    target_domain = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    pinned = Column(DateTime, nullable=True) # If null, not pinned
    saved_at = Column(DateTime, default=datetime.utcnow)
