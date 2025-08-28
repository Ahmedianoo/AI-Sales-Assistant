from sqlalchemy import Column, Integer, String, TIMESTAMP, DATE, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Report(Base):
    __tablename__ = 'reports'

    report_id = Column(Integer, primary_key=True)
    user_comp_id = Column(Integer, ForeignKey('user_competitors.user_comp_id', ondelete='CASCADE'))
    report_type = Column(String(50))
    report_date = Column(DATE, default=datetime.date.today)
    metrics = Column(JSONB)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)

    # Relationship
    user_competitor = relationship("UserCompetitor", back_populates="reports")

    def __repr__(self):
        return f"<Report(report_id={self.report_id}, type='{self.report_type}')>"