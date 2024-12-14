from utils.mysql_util import MySQLUtil
import os
from unittest import mock
from sqlalchemy import text

if os.getenv('DOCKER_TESTS') == 'True':
    mst = MySQLUtil()
else:
    mst = MySQLUtil('localhost', 3307, 'testuser', 'test', 'testdb')

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
        engine = mst.get_engine()
        connection = engine.connect()
        connection.execute(text('select 1'))
        connection.close()
        engine.dispose()
        assert True
    except Exception:
        assert False

def test_session_setup():
    try:
        session = mst.get_session()
        session.begin()
        session.close()
        assert True
    except Exception:
        assert False

def test_connection():
    try:
        conn = mst.get_connection()
        conn.close()
        assert True
    except Exception:
        assert False

def test_execution_raw_query():
    try:
        mst.execute_raw_query('select 1;')
        assert True
    except Exception:
        assert False

def test_get_data():
    query = 'Select 1 as test_nb;'
    data = mst.get_data(query)
    assert data[0][0] == 1

def test_get_df():
    query = 'Select 1 as test_nb, 2 as test_col2;'
    df = mst.get_df(query)
    expected_cols = ['test_nb', 'test_col2']

    for cols in df.columns:
        assert cols in expected_cols