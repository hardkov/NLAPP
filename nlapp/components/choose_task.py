import streamlit as st
from nlapp.service.task_type import TaskType


def task_print(task):
    return task.name


def write():
    st.header("Select task")
    task = st.radio("Task", list(TaskType), format_func=task_print)

    return task
