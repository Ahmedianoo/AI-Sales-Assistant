from sqlalchemy import Column, Integer, String, TIMESTAMP, JSONB, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Battlecard(Base):
    __tablename__ = 'battlecards'

    battlecard_id = Column(Integer, primary_key=True)
    user_comp_id = Column(Integer, ForeignKey('user_competitors.user_comp_id', ondelete='CASCADE'))
    title = Column(String(200))
    content = Column(JSONB)
    auto_release = Column(BOOLEAN, default=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)

    # Relationship
    user_competitor = relationship("UserCompetitor", back_populates="battlecards")

    
    def __repr__(self):
        return f"<Battlecard(battlecard_id={self.battlecard_id}, title='{self.title}')>"