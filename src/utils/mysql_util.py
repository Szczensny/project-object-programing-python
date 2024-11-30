from sqlalchemy import create_engine, Engine
from sqlalchemy.engine import Connection, Row, CursorResult
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import text
import pandas as pd
from typing import Sequence
import os

class MySQLUtil():
    def __init__(self, host:str=None, port:str=None, username:str=None, password:str=None, db_name:str=None):
        self.host = os.getenv('MYSQL_HOST') if host is None else host
        self.port = os.getenv('MYSQL_PORT') if port is None else port
        self.username = os.getenv('MYSQL_USERNAME') if username is None else username
        self.password = os.getenv('MYSQL_PASSWORD') if password is None else password
        self.db_name = os.getenv('MYSQL_DB_NAME') if db_name is None else db_name
        self.connection_url = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        if self.host is None or self.port is None or self.username is None or self.password is None or self.db_name is None:
            raise ValueError('Connection values to DB has not been provided')

    def get_engine(self) -> Engine:
        engine = create_engine(self.connection_url)
        return engine

    def get_session(self) -> Session:
        engine = self.get_engine()
        sn = sessionmaker(bind=engine)
        return sn()  
      
    def get_connection(self) -> Connection:
        engine = create_engine(self.connection_url)
        connection = engine.connect()
        return connection
    
    def execute_raw_query(self, query:str) -> CursorResult:
        conn = self.get_connection()
        result = conn.execute(text(query))
        conn.close()
        return result
    
    def get_data(self, query:str) -> Sequence[Row]:
        conn = self.get_connection()
        result = conn.execute(text(query))
        conn.close()
        return result.fetchall()
    
    def get_df(self, query:str) -> pd.DataFrame:
        conn = self.get_connection()
        df = pd.read_sql(sql=query, con=conn)
        conn.close()
        return df
