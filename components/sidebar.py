import streamlit as st

def write():
  st.sidebar.title("Pages")
  st.sidebar.selectbox("", ["Evaluation", "Statistics", "Train model", "About"])