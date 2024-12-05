import streamlit as st
from utils.mysql_util import MySQLUtil
from habits.habit import Habit
import time
ms = MySQLUtil().get_session()

@st.dialog("edit habit", width='large')
def edit(habit:Habit):
    with st.form(key='edit_habit'):
        st.write(habit.name)
        st.write(habit.uuid)
        name = st.text_input('New name ')
        submit = st.form_submit_button('update habit')
        if submit:
            habit.update_habit_name(ms, name)
            st.success('Name has been changed')
            time.sleep(2)
            st.rerun()

@st.dialog("delete habit", width='large')
def delete(habit:Habit):
    with st.form(key='edit_habit'):
        st.write(f'Are you sure that you want to delete habit: {habit.name}')
        delete_button = st.form_submit_button('Yes, please delete it.')
        if delete_button:
            habit.delete_habit(ms)
            st.success('Habit has been deleted')
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


select_frequency = st.selectbox('What kind of habbits would you like to see?',['All', 'Daily', 'Weekly'])
habits = Habit.get_all_habits(ms)
st.empty()

if select_frequency == 'All':
    data = [habit for habit in habits]
elif select_frequency == 'Daily':
    data = [habit for habit in habits if habit.frequency == 'daily']
elif select_frequency == 'Weekly':
     data = [habit for habit in habits if habit.frequency == 'weekly']

with st.container():
    col1, col2, col3, col4 = st.columns(4)
    col1.write('Habit name')
    col2.write('Habit frequency')
    col3.write('')
    col4.write('')
st.empty()
for habit in data:
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.write(habit.name)
        col2.write(habit.frequency)
        col3.empty()
        with col3:
            edit = st.button('Edit', key=f'edit_{habit.uuid}', on_click=edit, args=[habit])
        with col4:
            delete = st.button('delete',key=f'delete_{habit.uuid}', on_click=delete, args=[habit])

