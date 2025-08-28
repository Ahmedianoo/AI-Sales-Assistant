from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class UserCompetitor(Base):
    __tablename__ = 'user_competitors'

    user_comp_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    competitor_id = Column(Integer, ForeignKey('competitors.competitor_id', ondelete='CASCADE'))
    report_frequency = Column(String(50), default='monthly')
    battlecard_frequency = Column(String(50), default='monthly')
    
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)

    __table_args__ = (
        UniqueConstraint('user_id', 'competitor_id'),
    )

    # Relationships
    user = relationship("User", back_populates="user_competitors")
    competitor = relationship("Competitor", back_populates="users")
    reports = relationship("Report", back_populates="user_competitor", cascade="all, delete-orphan")
    battlecards = relationship("Battlecard", back_populates="user_competitor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserCompetitor(user_comp_id={self.user_comp_id})>"