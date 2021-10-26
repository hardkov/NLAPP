import streamlit as st

from nlapp.data_model.state import KEYS


def write(pages):
    st.sidebar.title("Pages")
    page = st.sidebar.selectbox(
        "Select page",
        pages,
        key = KEYS.SELECTED_PAGE,
        help="When you change page downloaded models and datasets will remain but selections will disapear",
    )
