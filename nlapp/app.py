import streamlit as st

import nlapp.view.pages.main_page as main_page

st.set_page_config(page_title="NLAPP", page_icon=":cat", layout="wide")


def main():
    main_page.write()


if __name__ == "__main__":
    main()
