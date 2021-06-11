import streamlit as st
from api.datasets.task_type import TaskType

def write():
  st.header("Select task")
  task = st.radio("Task", [task_type.name for task_type in TaskType])

  return task