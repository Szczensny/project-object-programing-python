from __future__ import annotations
import datetime
from habits.db_models import HabitDB, HabitEventDB
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound 
from typing import Union, List

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
    
    def update_habit_name(self, session:Session, name:str) -> None:
        session.query(HabitDB).filter(HabitDB.uuid == self.uuid).update({HabitDB.name: name})
        session.commit()
        self.name = name

    def delete_habit(self, session:Session) -> None:
        session.query(HabitDB).filter(HabitDB.uuid == self.uuid).delete()
        session.commit()





