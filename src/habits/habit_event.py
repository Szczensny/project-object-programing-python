import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.utils.db_base import BASE

class HabitEvent(BASE):
    __tablename__ = 'HABIT_EVENT'
    uuid = Column(String(46), primary_key=True)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    event_year = Column(Integer(), nullable=False)
    week_nb = Column(Integer(), nullable=False)
    habit_uuid = Column(String(46), ForeignKey('HABIT.uuid'))

