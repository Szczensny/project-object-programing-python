from utils.mysql_util import MySQLUtil
from habits.db_models import BASE, HabitDB, HabitEventDB
from habits.habit import Habit
import logging
from uuid import uuid4
import datetime
from typing import List
import os


def is_table_existing(table_name:str) -> bool:
    """Chekc if table with given name exist in the database

    Args:
        table_name (str): 

    Returns:
        bool: 
    """
    logging.info(f'Checking existence of table {table_name}')
    query = f"select count(*) as nb_tables from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='habbitapp' and TABLE_NAME='{table_name}';"
    result = ms.get_data(query)
    if result[0][0] > 0:
        logging.info(f'Table {table_name} exists.')
        return True
    else:
        logging.info(f'Table {table_name} does not exists.')
        return False

def create_table(table_name:str) -> None:
    """Creates table with given name

    Args:
        table_name (str): 
    """
    engine = ms.get_engine()
    if not is_table_existing(table_name):
        logging.info(f'Table {table_name} is not existing. creating.')
        BASE.metadata.tables[table_name].create(engine)
        logging.info(f'Table {table_name} has been created.')

def create_habbit(habit_name:str, frequency:str) -> Habit:
    """Create habit with given name and frequency

    Args:
        habit_name (str): 
        frequency (str): 

    Returns:
        Habit: 
    """
    session = ms.get_session()
    if not Habit.is_habit_existing(session, habit_name):
        h1 = Habit.create_habbit(session, uuid=str(uuid4()), name=habit_name, frequency=frequency)
    else:
        h1 = Habit.get_habit_by_name(session, habit_name)
    logging.info(str(h1))
    return h1

def create_habit_events(habit:Habit, event_times:List[datetime.datetime]) -> None:
    """Creates entries in database for given habit events

    Args:
        habit (Habit): 
        event_times (List[datetime.datetime]): 
    """
    session = ms.get_session()
    existing_list = habit.get_habit_events(session)
    if len(existing_list) == 0:
        habit.create_habit_event(session, event_times[0])
        existing_list = habit.get_habit_events(session)
    existing_ts_list = [he.created_at for he in existing_list]
    for event in event_times:
        if event not in existing_ts_list:
            habit.create_habit_event(session, event)

def execute():
    """Main execution point of the script
    """
    if not is_table_existing('HABIT'):
        create_table('HABIT')

    if not is_table_existing('HABIT_EVENT'):
        create_table('HABIT_EVENT')
    
    h1 = create_habbit('Homemade lunch', 'daily')
    h2 = create_habbit('Reading for 30 min', 'daily')
    h3 = create_habbit('Walking for 30 min', 'daily')
    h4 = create_habbit('Swimming training', 'weekly')
    h5 = create_habbit('Language learning session', 'weekly')

    h1_dates = [
        datetime.datetime(2024, 11, 1, 12, 5),
        datetime.datetime(2024, 11, 3, 12, 5),
        datetime.datetime(2024, 11, 6, 12, 5),
        datetime.datetime(2024, 11, 7, 12, 5),
        datetime.datetime(2024, 11, 8, 12, 5),
        datetime.datetime(2024, 11, 12, 12, 5),
        datetime.datetime(2024, 11, 13, 12, 5),
        datetime.datetime(2024, 11, 14, 12, 5),
        datetime.datetime(2024, 11, 15, 12, 5),
        datetime.datetime(2024, 11, 27, 12, 5),
        datetime.datetime(2024, 11, 28, 12, 5),
        datetime.datetime(2024, 11, 30, 12, 5)
    ]

    h2_dates = [
        datetime.datetime(2024, 11, 1, 12, 5),
        datetime.datetime(2024, 11, 4, 12, 5),
        datetime.datetime(2024, 11, 5, 12, 5),
        datetime.datetime(2024, 11, 6, 12, 5),
        datetime.datetime(2024, 11, 7, 12, 5),
        datetime.datetime(2024, 11, 8, 12, 5),
        datetime.datetime(2024, 11, 9, 12, 5),
        datetime.datetime(2024, 11, 10, 12, 5),
        datetime.datetime(2024, 11, 15, 12, 5),
        datetime.datetime(2024, 11, 20, 12, 5),
        datetime.datetime(2024, 11, 21, 12, 5),
        datetime.datetime(2024, 11, 30, 12, 5)
    ]

    h3_dates = [
        datetime.datetime(2024, 11, 1, 12, 5),
        datetime.datetime(2024, 11, 2, 12, 5),
        datetime.datetime(2024, 11, 3, 12, 5),
        datetime.datetime(2024, 11, 4, 12, 5),
        datetime.datetime(2024, 11, 5, 12, 5),
        datetime.datetime(2024, 11, 16, 12, 5),
        datetime.datetime(2024, 11, 17, 12, 5),
        datetime.datetime(2024, 11, 18, 12, 5),
        datetime.datetime(2024, 11, 19, 12, 5),
        datetime.datetime(2024, 11, 28, 12, 5),
        datetime.datetime(2024, 11, 29, 12, 5),
        datetime.datetime(2024, 11, 30, 12, 5)
    ]

    h4_dates = [
        datetime.datetime(2024, 11, 1, 12, 5),
        datetime.datetime(2024, 11, 7, 12, 5),
        datetime.datetime(2024, 11, 14, 12, 5),
        datetime.datetime(2024, 11, 30, 12, 5)
    ]

    h5_dates = [
        datetime.datetime(2024, 11, 1, 12, 5),
        datetime.datetime(2024, 11, 12, 12, 5),
        datetime.datetime(2024, 11, 21, 12, 5),
        datetime.datetime(2024, 11, 30, 12, 5)
    ]

    create_habit_events(h1, h1_dates)
    create_habit_events(h2, h2_dates)
    create_habit_events(h3, h3_dates)
    create_habit_events(h4, h4_dates)
    create_habit_events(h5, h5_dates)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if os.getenv('SKIP_EXAMPLES') == 'TRUE':
        logging.info('Skipping loading examples by ENV variable')
    else:
        ms = MySQLUtil()
        execute()