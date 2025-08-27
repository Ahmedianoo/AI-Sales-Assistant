from sqlalchemy import Column, Integer, String, TIMESTAMP, TEXT
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Competitor(Base):
    __tablename__ = 'competitors'

    competitor_id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    website_url = Column(TEXT, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)
    industry = Column(String(100))

    # Relationships
    users = relationship("UserCompetitor", back_populates="competitor")

    def __repr__(self):
        return f"<Competitor(competitor_id={self.competitor_id}, name='{self.name}')>"