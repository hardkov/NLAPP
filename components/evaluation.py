import streamlit as st

def write(task, model, dataset):
  st.title("This is evaluation")
  st.text(f"Evaluation = {task} + {model} + {dataset}")  