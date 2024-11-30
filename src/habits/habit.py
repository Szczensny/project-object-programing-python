
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime

from src.utils.db_base import BASE


class Habit(BASE):
    __tablename__ = 'HABIT'
    uuid = Column(String(46), primary_key=True)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    name = Column(String(100), nullable=False)
    frequency = Column(String(50))
    articles = relationship("HABIT_EVENT", backref='Habit')
