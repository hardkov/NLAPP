import streamlit as st

def write(pages):
  page_name = st.sidebar.radio("Choose page", list(pages.keys()))

  return page_name