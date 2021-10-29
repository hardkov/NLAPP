import streamlit as st

import nlapp.view.components.sidebar as sidebar
import nlapp.view.pages.evaluation_page as evaluation_page
import nlapp.view.pages.statistics_page as statistics_page
import nlapp.view.pages.train_model_page as train_model_page
import nlapp.view.pages.about_page as about_page
from nlapp.data_model.state import KEYS

apptitle = "NLAPP"
st.set_page_config(page_title=apptitle, page_icon=":cat", layout="wide")

PAGES = {
    "Evaluation": evaluation_page,
    "Statistics": statistics_page,
    "Train model": train_model_page,
    "About": about_page,
}


def main():
    sidebar.write(list(PAGES.keys()))

    current_page = st.session_state[KEYS.SELECTED_PAGE]
    PAGES[current_page].write()


if __name__ == "__main__":
    main()
