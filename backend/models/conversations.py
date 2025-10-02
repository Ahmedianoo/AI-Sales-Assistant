from sqlalchemy import Column, Integer, TEXT, TIMESTAMP, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Conversation(Base):
    __tablename__ = 'conversations'

    thread_id = Column(Uuid, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    title = Column(TEXT, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)

    # Relationship
    user = relationship("User", back_populates="conversations")
    
    def __repr__(self):
        return f"<Conversation(thread_id={self.thread_id}, user_id={self.user_id})>"