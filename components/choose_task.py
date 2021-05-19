import streamlit as st

def write():
  st.header("Select task")
  task = st.radio("Task", ["Fill mask", "Text classification"])

  return task