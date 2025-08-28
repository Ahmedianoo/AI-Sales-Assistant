from sqlalchemy import Column, Integer, TEXT, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Alert(Base):
    __tablename__ = 'alerts'

    alert_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    message = Column(TEXT, nullable=False)
    status = Column(String(20), default='pending')
    alert_type = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)

    # Relationship
    user = relationship("User", back_populates="alerts")

    def __repr__(self):
        return f"<Alert(alert_id={self.alert_id}, user_id={self.user_id}, status='{self.status}')>"