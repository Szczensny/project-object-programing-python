import streamlit as st
from utils.mysql_util import MySQLUtil
from habits.habit import Habit
from uuid import uuid4
ms = MySQLUtil().get_session()


with st.form('add_habit'):
    name = st.text_input('Habbit name')
    frequency = st.selectbox('Frequency', ['daily', 'weekly'])
    submit_button = st.form_submit_button('Add habit')

    if submit_button:
        Habit.create_habbit(
            session=ms,
            uuid=str(uuid4),
            name=name,
            frequency=frequency
        )
        st.success('Habbit has been added')