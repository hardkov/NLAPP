import streamlit as st


def write(pages):
    st.sidebar.title("Pages")
    page = st.sidebar.selectbox(
        "Select page",
        pages,
        help="When you change page downloaded models and datasets will remain but selections will disapear",
    )

    return page
