import streamlit as st
from utils.mysql_util import MySQLUtil
from habits.habit import Habit
from habits.db_models import HabitEventDB
from habits import analyis_functions as af

ms = MySQLUtil().get_session()



habits = Habit.get_all_habits(ms)
habits_with_events = []

for habit in habits:
    he = habit.get_habit_events(ms)
    habits_with_events.append((habit, he))

longest_strike = af.get_longest_strike_for_all_habits(habits_with_events)
col1, col2 = st.columns(2)
col1.metric("Habit with longest strike", longest_strike['habit_name'])
col2.metric("Longest strike count", longest_strike['strike'])
col1.metric("Longest strike from", longest_strike['min'].strftime("%d-%m-%Y"))
col2.metric("Longest strike from", longest_strike['max'].strftime("%d-%m-%Y"))

habits_counter = af.get_all_habits_counter(habits)
col1.metric("Daily habits", habits_counter["daily"])
col2.metric("Weekly habits", habits_counter["weekly"])


freq_chose = st.radio('Type of habits', ['all', 'daily', 'weekly'], horizontal=True)
if freq_chose == 'all':
    data = habits
else:
    data = af.get_all_habits_tracked_frequency(habits, freq_chose)

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.write('Habit name')
col2.write('Created at')
col3.write('Longest strike')
col4.write('Last strike')
col5.write('Last strike from')
col6.write('Last strike to')


for habit in data:
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.write(habit.name)
    col2.write(habit.created_at)
    he = habit.get_habit_events(ms)
    longest_strike = af.get_longest_strike(habit, he)
    last_stike = af.get_last_strike(habit, he)
    if longest_strike is not None:
        col3.write(longest_strike['max_strike_times'])
        col4.write(last_stike['strike'])
        col5.write(last_stike['min'].strftime("%d-%m-%Y"))
        col6.write(last_stike['max'].strftime("%d-%m-%Y"))
    else:
        col3.write('#N/A')
        col4.write('#N/A')
        col5.write('#N/A')
        col6.write('#N/A')
