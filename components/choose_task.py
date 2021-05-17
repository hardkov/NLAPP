import streamlit as st

def write():
  st.title("This is choose_task")
  task = st.radio("Task", ["Fill mask", "Text classification"])

  return task