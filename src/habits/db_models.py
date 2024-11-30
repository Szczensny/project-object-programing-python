import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

BASE = declarative_base()

class Habit(BASE):
    __tablename__ = 'HABIT'
    uuid = Column(String(46), primary_key=True)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    name = Column(String(100), nullable=False)
    frequency = Column(String(50))
    articles = relationship("HABIT_EVENT", backref='Habit')


class HabitEvent(BASE):
    __tablename__ = 'HABIT_EVENT'
    uuid = Column(String(46), primary_key=True)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    event_year = Column(Integer(), nullable=False)
    week_nb = Column(Integer(), nullable=False)
    habit_uuid = Column(String(46), ForeignKey('HABIT.uuid'))


