from utils.mysql_util import MySQLUtil
from habits.habit import Habit


ms = MySQLUtil().get_session()
try:
    Habit.create_habbit(ms, 'test', 'testname', 'daily')
except ValueError:
    print('already tere ')

h1 = Habit.create_habbit(ms, 'test4', 'testname4', 'daily')
h2 = Habit.create_habbit(ms, 'test3', 'testname3', 'daily')

h3 = Habit.get_habbit_by_uuid(ms,'test')
h4 = Habit.get_habbit_by_uuid(ms,'test2')

h5 = Habit.get_all_habits(ms)

h5 = [str(h) for h in h5]

print(h1)
print(h2)
print(h3)
print(h4)
print(h5)


h2.delete_habit(ms)
h3.update_habit_name(ms, 'new_habbit_name')

h5 = Habit.get_all_habits(ms)

h5 = [str(h) for h in h5]
print(h5)