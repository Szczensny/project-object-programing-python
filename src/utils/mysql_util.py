from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Row, CursorResult
from sqlalchemy import text
import pandas as pd
from typing import Sequence
import os

class MySQLUtil():
    def __init__(self, host:str=None, port:str=None, username:str=None, password:str=None, db_name:str=None):
        self.host = host if os.getenv('MYSQL_HOST') is None else os.getenv('MYSQL_HOST')
        self.port = port if os.getenv('MYSQL_PORT') is None else os.getenv('MYSQL_PORT')
        self.username = username if os.getenv('MYSQL_USERNAME') is None else os.getenv('MYSQL_USERNAME')
        self.password = password if os.getenv('MYSQL_PASSWORD') is None else os.getenv('MYSQL_PASSWORD')
        self.db_name = db_name if os.getenv('MYSQL_DB_NAME') is None else os.getenv('MYSQL_DB_NAME')
        self.connection_url = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        print(self.connection_url)
        if self.host is None or self.port is None or self.username is None or self.password is None or self.db_name is None:
            raise ValueError('Connection values to DB has not been provided')

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
