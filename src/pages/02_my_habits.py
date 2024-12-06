import streamlit as st
from utils.mysql_util import MySQLUtil
from habits.habit import Habit
import time
from uuid import uuid4
ms = MySQLUtil().get_session()

@st.dialog("add habit", width='large')
def add_habit():
    """adds popup that allows to add habit to db
    """
    name = st.text_input('Habbit name')
    frequency = st.selectbox('Frequency', ['daily', 'weekly'])
    submit_button = st.button('Add habit')
    if submit_button:
        try:
            Habit.create_habbit(
                session=ms,
                uuid=str(uuid4()),
                name=name,
                frequency=frequency
            )
            st.success('Habbit has been added')
        except ValueError:
            st.error(f'Habit with name: {name} is already existing!')
        finally:
            time.sleep(2)
            st.rerun()

@st.dialog("edit habit", width='large')
def edit(habit:Habit):
    """adds popup that allows to edit habit name

    Args:
        habit (Habit): habit object in intrest
    """
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
    """adds popup that allows to delete habit.

    Args:
        habit (Habit): habit object in intrest
    """
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

add_button = st.button('Add Habit', key=f'add_habit', on_click=add_habit)

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.write('Habit name')
    col2.write('Habit frequency')
    col3.write('Created at')
    col4.write('')
    col5.empty()
st.empty()
for habit in data:
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write(habit.name)
        col2.write(habit.frequency)
        col3.write(habit.created_at)
        with col4:
            edit_button = st.button('Edit', key=f'edit_{habit.uuid}', on_click=edit, args=[habit])
        with col5:
            delete_buttpm = st.button('delete',key=f'delete_{habit.uuid}', on_click=delete, args=[habit])

