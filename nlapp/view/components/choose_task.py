import streamlit as st
from nlapp.data_model.task_type import TaskType


def task_print(task):
    return task.name


def write():
    st.header("Select task")
    task = st.radio("Task", list(TaskType), format_func=task_print)

    return task
