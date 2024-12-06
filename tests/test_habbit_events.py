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

def test_habbit_event_creation():
    recreate_tables()
    current_time = datetime.datetime.now()
    sleep(1)
    h1 = Habit.create_habbit(ms_session, 'test_uuid', 'test_habbit1', 'daily')
    he1 = h1.create_habit_event(ms_session)
    db_event = h1.get_habit_event_by_uuid(session=ms_session, habit_event_uuid=he1.uuid)
    try:
        he2 = h1.create_habit_event(ms_session)
        assert False
    except ValueError:
        assert True
    assert h1.uuid == db_event.habit_uuid
    assert db_event.created_at > current_time

def test_get_habit_events():
    h1 = Habit.create_habbit(ms_session, 'test_uuid2', 'test_habbit2', 'daily')
    he1 = h1.create_habit_event(ms_session)
    he2 = h1.create_habit_event(ms_session, datetime.datetime(2024, 11, 12))
    he3 = h1.create_habit_event(ms_session, datetime.datetime(2023, 11, 12))

    search1 = h1.get_habit_events(ms_session)
    search2 = h1.get_habit_events(ms_session, from_date=datetime.datetime(2024, 11, 20))
    search3 = h1.get_habit_events(ms_session, from_week_nb=40)
    s1_goted = [event.uuid for event in search1]
    s2_goted = [event.uuid for event in search2]
    s3_goted = [event.uuid for event in search3]

    try:
        search4 = h1.get_habit_events(ms_session,from_date=datetime.datetime(2024, 11, 20), from_week_nb=40)
    except ValueError:
        assert True
    assert len(search1) == 3
    assert len(search2) == 1
    assert len(search3) == 2
    assert he1.uuid in s1_goted
    assert he2.uuid in s1_goted
    assert he3.uuid in s1_goted
    assert he1.uuid in s2_goted
    assert he2.uuid not in s2_goted
    assert he3.uuid not in s2_goted
    assert he1.uuid in s3_goted
    assert he2.uuid in s3_goted
    assert he3.uuid not in s3_goted

def test_delete_habbit_evnet():
    recreate_tables()
    h1 = Habit.create_habbit(ms_session, 'test_uuid12', 'test_habbit12', 'daily')
    he1 = h1.create_habit_event(ms_session)
    db_event = h1.get_habit_event_by_uuid(session=ms_session, habit_event_uuid=he1.uuid)
    assert he1.uuid == db_event.uuid
    h1.delete_habit_event(ms_session, he1.uuid)
    db_event2 = h1.get_habit_event_by_uuid(session=ms_session, habit_event_uuid=he1.uuid)
    assert db_event2 is None