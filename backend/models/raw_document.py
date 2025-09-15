from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class RawDocument(Base):
    __tablename__ = "raw_documents"

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.competitor_id"), nullable=False)
    text = Column(Text, nullable=False)
    scraped_at = Column(TIMESTAMP, default=datetime.datetime.now) #the only line i added + its imports above

    # Relationship back to Competitor
    competitor = relationship("Competitor", back_populates="documents")
