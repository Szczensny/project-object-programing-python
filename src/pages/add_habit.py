import streamlit as st
from utils.mysql_util import MySQLUtil
from habits.habit import Habit
from uuid import uuid4
import time
ms = MySQLUtil().get_session()


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
