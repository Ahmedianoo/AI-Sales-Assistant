from sqlalchemy import Column, Integer, String, TIMESTAMP, TEXT
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(TEXT, nullable=False)
    plan_type = Column(String(50), default='free')
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)

    # Relationships
    user_competitors = relationship(
        "UserCompetitor",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    search_history = relationship(
        "SearchHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    alerts = relationship(
        "Alert",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(user_id={self.user_id}, email='{self.email}')>"