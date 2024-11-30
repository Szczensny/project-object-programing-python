from src.utils.mysql_util import MySQLUtil
from src.habits.db_models import BASE, Habit, HabitEvent
import pytest 
import os
from unittest import mock
from sqlalchemy import text

@pytest.fixture(scope="module")
def db_session():
    mysql = MySQLUtil('localhost', 3306, 'testuser', 'test', 'testdb')
    engine = mysql.get_engine()
    session = mysql.get_session()

    BASE.metadata.create_all(bind = engine)
    yield session
    session.close()
    BASE.metadata.drop_all(bind=engine)

def test_dupa ():
    assert 1==1

def test_db_object_setup_correct():
    ms = MySQLUtil('localhost', '5555', 'example_user', 'example_passowrd', 'example_db')
    assert ms.host == 'localhost'
    assert ms.port == '5555'
    assert ms.username == 'example_user'
    assert ms.password == 'example_passowrd'
    assert ms.db_name == 'example_db'

@mock.patch.dict(os.environ, clear=True)
def test_db_setup_no_data():
    try:
        ms = MySQLUtil()
    except ValueError:
        assert True

def test_engine_setup():
    try:
        ms = MySQLUtil('localhost', 3306, 'testuser', 'test', 'testdb')
        engine = ms.get_engine()
        connection = engine.connect()
        connection.execute(text('select 1'))
        assert True
    except Exception:
        assert False

def test_session_setup():
    try:
        ms = MySQLUtil('localhost', 3306, 'testuser', 'test', 'testdb')
        session = ms.get_session()
        session.begin()
        session.close()
        assert True
    except Exception:
        assert False

def test_connection():
    try:
        ms = MySQLUtil('localhost', 3306, 'testuser', 'test', 'testdb')
        conn = ms.get_connection()
        conn.close()
        assert True
    except Exception:
        assert False

def test_execution_raw_query():
    ms = MySQLUtil('localhost', 3306, 'testuser', 'test', 'testdb')
    try:
        ms.execute_raw_query('select 1;')
        assert True
    except Exception:
        assert False

def test_get_data():
    query = 'Select 1 as test_nb;'
    ms = MySQLUtil('localhost', 3306, 'testuser', 'test', 'testdb')
    data = ms.get_data(query)
    assert data[0][0] == 1

def test_get_df():
    query = 'Select 1 as test_nb, 2 as test_col2;'
    ms = MySQLUtil('localhost', 3306, 'testuser', 'test', 'testdb')
    df = ms.get_df(query)
    expected_cols = ['test_nb', 'test_col2']

    for cols in df.columns:
        assert cols in expected_cols