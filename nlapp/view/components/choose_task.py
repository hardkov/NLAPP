import streamlit as st

from nlapp.data_model.state import KEYS
from nlapp.data_model.task_type import TaskType


def task_print(task_name):
    task: TaskType = TaskType[task_name]
    return task.display_name()


def write():
    st.header("Select task")

    tasks, _, description = st.columns([6, 1, 5])

    with tasks:
        tasks_names = list(map(lambda t: t.name, list(TaskType)))
        task_name = st.radio(
            "Tasks", tasks_names, key=KEYS.SELECTED_TASK, format_func=task_print
        )
        task: TaskType = TaskType[task_name]

    with description:
        st.subheader("Task Description")
        st.markdown(task.description())
