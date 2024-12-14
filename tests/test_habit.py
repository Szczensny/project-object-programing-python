from utils.mysql_util import MySQLUtil
from habits.habit import Habit
import datetime
from time import sleep
from habits.db_models import BASE, HabitDB, HabitEventDB
import logging
import os

if os.getenv('DOCKER_TESTS') == 'True':
    ms = MySQLUtil()
else:
    ms = MySQLUtil('localhost', 3307, 'testuser', 'test', 'testdb')

ms_session = ms.get_session()
engine = ms.get_engine()

BASE.metadata.create_all(engine)

def recreate_tables():
    ms.execute_raw_query('delete from HABIT_EVENT where 1=1;')
    ms.execute_raw_query('delete from HABIT where 1=1;')


def test_habbit_creation():
    recreate_tables()
    current_time = datetime.datetime.now()
    sleep(1)
    h1 = Habit.create_habbit(ms_session, 'test_uuid', 'test_habbit1', 'daily')
    assert h1.name == 'test_habbit1'
    assert h1.uuid == 'test_uuid'
    assert h1.frequency == 'daily'
    assert h1.created_at > current_time
    assert str(h1) == f'UUID: test_uuid, name: test_habbit1, frequency: daily, created_at: {h1.created_at}'
    h1.delete_habit(ms_session)

def test_habbit_creation_already_exists():
    recreate_tables()
    try:
        h1 = Habit.create_habbit(ms_session, 'test_uuid3', 'test_habbit3', 'daily')
        h2 = Habit.create_habbit(ms_session, 'test_uuid3', 'test_habbit3', 'daily')
    except ValueError:
        assert True

def test_get_habbit_by_name():
    recreate_tables()
    h1 = Habit.create_habbit(ms_session, 'test_uuid44', 'test_habbit44', 'daily')
    h2 = Habit.get_habit_by_name(ms_session,'test_habbit44')
    h3 = Habit.get_habit_by_name(ms_session,'test_habbit444')

    assert h1.name == h2.name
    assert h1.created_at == h2.created_at
    assert h1.frequency == h2.frequency
    assert h1.uuid == h2.uuid
    assert h3 is None
    
def test_get_habbit_by_uuid():
    recreate_tables()
    h1 = Habit.create_habbit(ms_session, 'test_uuid4', 'test_habbit4', 'daily')
    h2 = Habit.get_habbit_by_uuid(ms_session,'test_uuid4')
    assert h1.name == h2.name
    assert h1.created_at == h2.created_at
    assert h1.frequency == h2.frequency
    assert h1.uuid == h2.uuid

def test_get_all_habits():
    recreate_tables()
    h1 = Habit.create_habbit(ms_session, 'test_uuid5', 'test_habbit5', 'daily')
    h2 = Habit.create_habbit(ms_session, 'test_uuid6', 'test_habbit6', 'daily')
    h3 = Habit.create_habbit(ms_session, 'test_uuid7', 'test_habbit7', 'daily')
    h4 = Habit.create_habbit(ms_session, 'test_uuid8', 'test_habbit8', 'daily')
    all_habbits = Habit.get_all_habits(ms_session)
    list_lenght = len(all_habbits)
    assert list_lenght == 4
    for row in all_habbits:
        assert row.name in ['test_habbit5','test_habbit6', 'test_habbit7', 'test_habbit8']

def test_is_habbit_existing():
    recreate_tables()
    h1 = Habit.create_habbit(ms_session, 'test_uuid9', 'test_habbit9', 'daily')
    t1 = Habit.is_habit_existing(ms_session, 'test_habbit10')
    t2 = Habit.is_habit_existing(ms_session, 'test_habbit9')
    assert t1 == False
    assert t2 == True

def test_update_habbit_name():
    h1 = Habit.create_habbit(ms_session, 'test_uuid11', 'test_habbit11', 'daily')
    assert h1.name == 'test_habbit11'
    h1.update_habit_name(ms_session, 'that_is_new_name')
    h2 = Habit.get_habbit_by_uuid(ms_session, h1.uuid)
    assert h1.name == 'that_is_new_name'
    assert h2.name == 'that_is_new_name'

def test_delete_habbit():
    h1 = Habit.create_habbit(ms_session, 'test_uuid12', 'test_habbit12', 'daily')
    h2 = Habit.get_habbit_by_uuid(ms_session, h1.uuid)
    assert h1.uuid == h2.uuid
    h1.delete_habit(ms_session)
    h2 = Habit.get_habbit_by_uuid(ms_session, h1.uuid)
    assert h2 is None