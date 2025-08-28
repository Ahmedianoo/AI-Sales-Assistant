from sqlalchemy import Column, Integer, TEXT, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class SearchHistory(Base):
    __tablename__ = 'search_history'

    search_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    query = Column(TEXT, nullable=False)
    searched_at = Column(TIMESTAMP, default=datetime.datetime.now)

    # Relationship
    user = relationship("User", back_populates="search_history")
    
    def __repr__(self):
        return f"<SearchHistory(search_id={self.search_id}, user_id={self.user_id})>"