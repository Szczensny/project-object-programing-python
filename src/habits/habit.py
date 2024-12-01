from __future__ import annotations
import datetime
from habits.db_models import HabitDB, HabitEventDB
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound 
from sqlalchemy import select, cast, Date
from typing import Union, List
from uuid import uuid4
import logging

class Habit():
    def __init__(self, uuid:str, name:str, frequency:str, created_at):
        self.uuid = uuid
        self.name = name
        self.frequency = frequency
        self.created_at = created_at
    
    def __str__(self):
        return f'UUID: {self.uuid}, name: {self.name}, frequency: {self.frequency}, created_at: {self.created_at}'
        
    @staticmethod
    def create_habbit(session:Session, uuid:str, name:str, frequency:str) -> Habit:
        if not Habit.is_habit_existing(session, name):
            new_habit = HabitDB(uuid=uuid, name=name, frequency=frequency, created_at=datetime.datetime.now())
            session.add(new_habit)
            session.commit()
            return Habit.get_habbit_by_uuid(session, uuid)
        else:
            raise ValueError(f'Habit with name: {name} is already existing!')
    
    @staticmethod
    def get_habbit_by_uuid(session:Session, uuid:str) -> Union[Habit, None]:
        try:
            result = session.query(HabitDB).filter(HabitDB.uuid == uuid).one()
            session.close()
            return Habit(result.uuid, result.name, result.frequency, result.created_at)
        except NoResultFound:
            return None
    
    @staticmethod
    def get_all_habits(session:Session) -> List[Habit]:
        result = session.query(HabitDB).all()
        habits = []
        for row in result:
            habits.append(Habit(row.uuid, row.name, row.frequency, row.created_at))
        return habits
    
    @staticmethod
    def is_habit_existing(session:Session, name:str) -> bool:
        try:
            session.query(HabitDB).filter(HabitDB.name == name).one()
            return True
        except NoResultFound:
            return False
    @staticmethod
    def get_habit_by_name(session:Session, name:str) -> Habit:
        try:
            result = session.query(HabitDB).filter(HabitDB.name == name).one()
            return Habit(result.uuid, result.name, result.frequency, result.created_at)
        except NoResultFound:
            return None
    
    def update_habit_name(self, session:Session, name:str) -> None:
        session.query(HabitDB).filter(HabitDB.uuid == self.uuid).update({HabitDB.name: name})
        session.commit()
        self.name = name

    def delete_habit(self, session:Session) -> None:
        session.query(HabitEventDB).filter(HabitEventDB.habit_uuid == self.uuid).delete()
        session.query(HabitDB).filter(HabitDB.uuid == self.uuid).delete()
        session.commit()

    def get_habit_event_by_date(self, session:Session, date:datetime.date) -> HabitEventDB:
        try:
            result = session.query(HabitEventDB).filter(cast(HabitEventDB.created_at, Date)== date).filter(HabitEventDB.habit_uuid==self.uuid).one()
            return result
        except NoResultFound:
            return None

    def create_habit_event(self, session:Session, event_ts:datetime.datetime=None) -> HabitEventDB:
        current_ts = datetime.datetime.now() if event_ts is None else event_ts
        if self.get_habit_event_by_date(session, current_ts.date()) is not None:
            raise ValueError('Habit event for that day is already existing!')
        new_habbit_event = HabitEventDB(uuid=str(uuid4()), created_at=current_ts, event_year=current_ts.year, week_nb=current_ts.strftime("%V"), habit_uuid=self.uuid)
        session.add(new_habbit_event)
        session.commit()
        return new_habbit_event
    
    def get_habit_event_by_uuid(self, session:Session, habit_event_uuid:str) -> HabitEventDB:
        try:
            result = session.query(HabitEventDB).filter(HabitEventDB.uuid==habit_event_uuid).one()
            return result
        except NoResultFound:
            return None
    
    def get_habit_events(self, session:Session, from_date:datetime.datetime=None, from_week_nb:int=None, year:int=None) -> List[HabitEventDB]:
        if from_date is not None and from_week_nb is not None:
            raise ValueError('You can choose only from_date or from_week_nb as fiter')
        
        if from_date is not None:
            statement = select(HabitEventDB).filter(HabitEventDB.habit_uuid == self.uuid).filter(HabitEventDB.created_at >= from_date)
        elif from_week_nb is not None:
            year = year if year is not None else datetime.datetime.now().year
            logging.warning(year)
            statement = select(HabitEventDB).filter(HabitEventDB.habit_uuid == self.uuid).filter(HabitEventDB.week_nb >= from_week_nb).filter(HabitEventDB.event_year == year)
        else:
            statement = select(HabitEventDB).filter(HabitEventDB.habit_uuid == self.uuid)
        result = session.execute(statement=statement).all()
        return [item[0] for item in result]
    
    def delete_habit_event(self, session:Session, habit_event_uuid:str):
        session.query(HabitEventDB).filter(HabitEventDB.uuid == habit_event_uuid).delete()
        session.commit()




