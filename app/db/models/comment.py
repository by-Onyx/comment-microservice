from sqlalchemy import Column, Integer, VARCHAR, CheckConstraint, DateTime, SmallInteger
from app.db.base import Base
from datetime import datetime


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    comment = Column(VARCHAR(1024), nullable=False)
    rating = Column(SmallInteger, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    product_id = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5', name='comment_check_rating_range'),
    )
