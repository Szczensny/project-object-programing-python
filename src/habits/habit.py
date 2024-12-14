from __future__ import annotations
import datetime
from habits.db_models import HabitDB, HabitEventDB
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound 
from sqlalchemy import select, cast, Date, desc
from typing import List
from uuid import uuid4

class Habit():
    """Class that holds all posible actions of habits and coresponding habits events.
    """
    def __init__(self, uuid:str, name:str, frequency:str, created_at:datetime.date):
        """Initialization function for creating habits. 

        Args:
            uuid (str): UUID of habit
            name (str): Name of the habit
            frequency (str): Frequency of habit [daily | weekly]
            created_at (datetime.date): time when habit was created
        """
        self.uuid = uuid
        self.name = name
        self.frequency = frequency
        self.created_at = created_at
    
    def __str__(self) -> str:
        """returns string representation of object

        Returns:
            str: 
        """
        return f'UUID: {self.uuid}, name: {self.name}, frequency: {self.frequency}, created_at: {self.created_at}'
        
    @staticmethod
    def create_habbit(session:Session, uuid:str, name:str, frequency:str) -> Habit:
        """Creation of habit object in Database

        Args:
            session (Session): Database session (sql alchemy)
            uuid (str): UUID of habit
            name (str): Name of the habit
            frequency (str): Frequency of habit [daily | weekly]

        Raises:
            ValueError: In case if habit with the same name already exists in the database

        Returns:
            Habit: newly created habit object
        """
        if not Habit.is_habit_existing(session, name):
            new_habit = HabitDB(uuid=uuid, name=name, frequency=frequency, created_at=datetime.datetime.now())
            session.add(new_habit)
            session.commit()
            return Habit.get_habbit_by_uuid(session, uuid)
        else:
            raise ValueError(f'Habit with name: {name} is already existing!')
    
    @staticmethod
    def get_habbit_by_uuid(session:Session, uuid:str) -> Habit | None:
        """Returns the habit object for habit with given uuid

        Args:
            session (Session): Database connection session (sql alchemy)
            uuid (str): UUID of habit

        Returns:
            Habit | None: Returns None if habit with given UUID does not exists in Database
        """
        try:
            result = session.query(HabitDB).filter(HabitDB.uuid == uuid).one()
            session.close()
            return Habit(result.uuid, result.name, result.frequency, result.created_at)
        except NoResultFound:
            return None
    
    @staticmethod
    def get_all_habits(session:Session) -> List[Habit]:
        """Extracts all existing habits in the database

        Args:
            session (Session): Database connection Session (sql alchemy)

        Returns:
            List[Habit]: List of habits in DB. Retruns empty list if there is no habits in DB
        """
        result = session.query(HabitDB).order_by(desc(HabitDB.created_at)).all()
        habits = []
        for row in result:
            habits.append(Habit(row.uuid, row.name, row.frequency, row.created_at))
        return habits
    
    @staticmethod
    def is_habit_existing(session:Session, name:str) -> bool:
        """Check if habbit with given name exist in the database

        Args:
            session (Session): Database connection session (sql alchemy)
            name (str): name of the habit

        Returns:
            bool: returns `True` if habit is already in database
        """
        try:
            session.query(HabitDB).filter(HabitDB.name == name).one()
            return True
        except NoResultFound:
            return False
    @staticmethod
    def get_habit_by_name(session:Session, name:str) -> Habit | None:
        """Extract the habit from database with given name

        Args:
            session (Session): Database connection session
            name (str): Name of the habit

        Returns:
            Habit | None: Returns conresponding `Habit` object. It there is no habit with given name returns `None`
        """
        try:
            result = session.query(HabitDB).filter(HabitDB.name == name).one()
            return Habit(result.uuid, result.name, result.frequency, result.created_at)
        except NoResultFound:
            return None
    
    def update_habit_name(self, session:Session, name:str) -> None:
        """Performs update of the habit name in database

        Args:
            session (Session): Database connection session (sql alchemy)
            name (str): New name of the habit
        """
        session.query(HabitDB).filter(HabitDB.uuid == self.uuid).update({HabitDB.name: name})
        session.commit()
        self.name = name

    def delete_habit(self, session:Session) -> None:
        """Deltes habit and all coresponding habit events from the database

        Args:
            session (Session): Database connection session (sql alchemy)
        """
        session.query(HabitEventDB).filter(HabitEventDB.habit_uuid == self.uuid).delete()
        session.query(HabitDB).filter(HabitDB.uuid == self.uuid).delete()
        session.commit()

    def get_habit_event_by_date(self, session:Session, date:datetime.date) -> HabitEventDB | None:
        """Returns the habit event for a given date

        Args:
            session (Session): Database connection session. 
            date (datetime.date): data of intrest

        Returns:
            HabitEventDB | None: Retruns the habit event object. If there is no entry in database returns `None`
        """
        try:
            result = session.query(HabitEventDB).filter(cast(HabitEventDB.created_at, Date)== date).filter(HabitEventDB.habit_uuid==self.uuid).one()
            return result
        except NoResultFound:
            return None

    def create_habit_event(self, session:Session, event_ts:datetime.datetime=None) -> HabitEventDB:
        """Creates habit event in the database. 

        Args:
            session (Session): database connection session (sql alchemy)
            event_ts (datetime.datetime, optional): _description_. Defaults to datetime.datetime.now().

        Raises:
            ValueError: In case that event is existing for habit for given day rise the `ValueError`

        Returns:
            HabitEventDB: retruns representation of habit event in DB
        """
        current_ts = datetime.datetime.now() if event_ts is None else event_ts
        if self.get_habit_event_by_date(session, current_ts.date()) is not None:
            raise ValueError('Habit event for that day is already existing!')
        new_habbit_event = HabitEventDB(uuid=str(uuid4()), created_at=current_ts, event_year=current_ts.year, week_nb=current_ts.strftime("%V"), habit_uuid=self.uuid)
        session.add(new_habbit_event)
        session.commit()
        return new_habbit_event
    
    def get_habit_event_by_uuid(self, session:Session, habit_event_uuid:str) -> HabitEventDB | None:
        """Returns the habit event with given UUID

        Args:
            session (Session): database connection session (sql alchemy)
            habit_event_uuid (str): UUID of habit event

        Returns:
            HabitEventDB | None: represention of habit event in database. It there is no entry returns `None`
        """
        try:
            result = session.query(HabitEventDB).filter(HabitEventDB.uuid==habit_event_uuid).one()
            return result
        except NoResultFound:
            return None
    
    def get_habit_events(self, session:Session, from_date:datetime.datetime=None, from_week_nb:int=None, year:int=None) -> List[HabitEventDB]:
        """Returns a list of habit events in the database in descending order. If no arguments are provied return all events in database

        Args:
            session (Session): database connection session (sql alchemy)
            from_date (datetime.datetime, optional): date from witch events should be returned. Defaults to None.
            from_week_nb (int, optional): week number from which data should be retruned. Defaults to None.
            year (int, optional): Year from wich events should be extacted. Defaults to None.

        Raises:
            ValueError: Only one filter can be used (eather `from_date` or both `from_week_nb` and `year`). If all of them provided rises and error

        Returns:
            List[HabitEventDB]: List of habits event from database
        """
        if from_date is not None and from_week_nb is not None:
            raise ValueError('You can choose only from_date or from_week_nb as fiter')
        
        if from_date is not None:
            statement = select(HabitEventDB).filter(HabitEventDB.habit_uuid == self.uuid).filter(HabitEventDB.created_at >= from_date).order_by(desc(HabitEventDB.created_at))
        elif from_week_nb is not None:
            year = year if year is not None else datetime.datetime.now().year
            statement = select(HabitEventDB).filter(HabitEventDB.habit_uuid == self.uuid).filter(HabitEventDB.week_nb >= from_week_nb).filter(HabitEventDB.event_year == year).order_by(desc(HabitEventDB.created_at))
        else:
            statement = select(HabitEventDB).filter(HabitEventDB.habit_uuid == self.uuid).order_by(desc(HabitEventDB.created_at))
        result = session.execute(statement=statement).all()
        return [item[0] for item in result]
    
    def delete_habit_event(self, session:Session, habit_event_uuid:str):
        """delete habit event from database with given uuid

        Args:
            session (Session): database connection session (sql alchemy)
            habit_event_uuid (str): habit event uuid
        """
        session.query(HabitEventDB).filter(HabitEventDB.uuid == habit_event_uuid).delete()
        session.commit()
