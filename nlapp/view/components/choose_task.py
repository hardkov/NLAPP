import streamlit as st

from nlapp.data_model.state import KEYS
from nlapp.data_model.task_type import TaskType


def task_print(task):
    return task.name


def write():
    st.header("Select task")
    st.radio("Task", list(TaskType), key=KEYS.SELECTED_TASK, format_func=task_print)

