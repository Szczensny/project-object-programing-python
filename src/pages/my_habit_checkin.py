import streamlit as st
from utils.mysql_util import MySQLUtil
from habits.habit import Habit
from habits.db_models import HabitEventDB
import time

ms = MySQLUtil().get_session()
st.title = 'My habits checkin'

@st.dialog("delete habit", width='large')
def delete(habit:Habit, habit_event:HabitEventDB):
    with st.form(key='edit_habit'):
        st.write(f'Are you sure that you want to delete habit event?')
        delete_button = st.form_submit_button('Yes, please delete it.')
        if delete_button:
            habit.delete_habit_event(ms, habit_event.uuid)
            st.success('Habit event has been deleted')
            time.sleep(2)
            st.rerun()

st.markdown("""
    <style>
    [data-testid="stVerticalBlock"]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)

def change_page():
    st.switch_page('pages/analysis.py')

habits = Habit.get_all_habits(ms)
habits_list = [habit.name for habit in habits]
select_habit = st.selectbox('What kind of habbits would you like to see?',habits_list)

st.empty()
habit = Habit.get_habit_by_name(ms, select_habit)
st.write(f'Habit: {habit.name}')
st.write(f'Habit frequency: {habit.frequency}')
st.write(f'Created at: {habit.created_at}')
habit_events = habit.get_habit_events(ms)

st.empty()
add_new_event = st.button('Add new event')
if add_new_event:
    try:
        habit.create_habit_event(ms)
        info = st.success('Added habit event!')
    except ValueError:
        info = st.error('Cannot add event as one exist for today already!')
    finally:
        time.sleep(2)
        st.rerun()

st.empty()

with st.container():
    col1, col2, col3 = st.columns(3)
    col1.write('checkin time')
    col2.write('')
    col3.write('')
st.empty()

for event in habit_events:
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        col1.write(event.created_at)
        col2.empty()
        with col3:
            delete_button = st.button('delete',key=f'delete_{event.uuid}', on_click=delete, args=[habit, event])

