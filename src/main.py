from sqlalchemy.orm import declarative_base
from utils.mysql_util import MySQLUtil
from utils.db_base import BASE
from habits.habit import Habit
from habits.habit_event import HabitEvent

msql = MySQLUtil()
BASE.metadata.create_all(msql.get_engine())