from sqlalchemy import create_engine, Engine
from sqlalchemy.engine import Connection, Row, CursorResult
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text
import pandas as pd
from typing import Sequence
import os

class MySQLUtil():
    """Class that allow to interact with the 
    """
    def __init__(self, host:str=None, port:str=None, username:str=None, password:str=None, db_name:str=None):
        """Iniciate object with required details.

        Args:
            host (str, optional): Database host. If not provided try to get if througg env variable `MYSQL_HOST`. Defaults to None.
            port (str, optional): Database port. If not provided try to get if througg env variable `MYSQL_PORT`. Defaults to None.
            username (str, optional): Database username. If not provided try to get if througg env variable `MYSQL_USERNAME`. Defaults to None.
            password (str, optional): Database password. If not provided try to get if througg env variable `MYSQL_PASSWORD`. Defaults to None.
            db_name (str, optional): Database name. If not provided try to get if througg env variable `MYSQL_DB_NAME`. Defaults to None.

        Raises:
            ValueError: If connection details are incomplete
        """
        self.host = os.getenv('MYSQL_HOST') if host is None else host
        self.port = os.getenv('MYSQL_PORT') if port is None else port
        self.username = os.getenv('MYSQL_USERNAME') if username is None else username
        self.password = os.getenv('MYSQL_PASSWORD') if password is None else password
        self.db_name = os.getenv('MYSQL_DB_NAME') if db_name is None else db_name
        self.connection_url = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        if self.host is None or self.port is None or self.username is None or self.password is None or self.db_name is None:
            raise ValueError('Connection values to DB has not been provided')

    def get_engine(self) -> Engine:
        """Returns engine for given connection

        Returns:
            Engine: Sql alchemy engine
        """
        engine = create_engine(self.connection_url).execution_options(auautocommit=True)
        return engine

    def get_session(self) -> Session:
        """Returns session to the database

        Returns:
            Session: Sql akchemy session
        """
        engine = self.get_engine()
        sn = sessionmaker(bind=engine, autoflush=True)
        return sn()  
      
    def get_connection(self) -> Connection:
        """Returns connection to the database

        Returns:
            Connection: Sql alchemy connection
        """
        engine = create_engine(self.connection_url)
        connection = engine.connect()
        return connection
    
    def execute_raw_query(self, query:str) -> CursorResult:
        """Returns the result of the query represented as string

        Args:
            query (str): sql query

        Returns:
            CursorResult: 
        """
        conn = self.get_connection()
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
        return result
    
    def get_data(self, query:str) -> Sequence[Row]:
        """returns the sequence of rows as reulst of the query

        Args:
            query (str): qurey string

        Returns:
            Sequence[Row]: 
        """
        conn = self.get_connection()
        result = conn.execute(text(query))
        conn.close()
        return result.fetchall()
    
    def get_df(self, query:str) -> pd.DataFrame:
        """returns reuslt of the query as Pandas Dataframe

        Args:
            query (str): Sql query

        Returns:
            pd.DataFrame: 
        """
        conn = self.get_connection()
        df = pd.read_sql(sql=query, con=conn)
        conn.close()
        return df
