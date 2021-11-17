import streamlit as st

from nlapp.data_model.state import KEYS
from nlapp.data_model.task_type import TaskType


def write():
    st.header("Select task")
    tasks_names = list(map(lambda t: t.name, list(TaskType)))
    st.radio(
        "Task", tasks_names, key=KEYS.SELECTED_TASK
    )
