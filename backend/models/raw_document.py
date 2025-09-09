from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class RawDocument(Base):
    __tablename__ = "raw_documents"

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.competitor_id"), nullable=False)
    text = Column(Text, nullable=False)

    # Relationship back to Competitor
    competitor = relationship("Competitor", back_populates="documents")
