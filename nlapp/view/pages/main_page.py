import streamlit as st

import nlapp.view.components.sidebar as sidebar
import nlapp.view.pages.evaluation_page as evaluation_page
import nlapp.view.pages.statistics_page as statistics_page
import nlapp.view.pages.train_model_page as train_model_page
import nlapp.view.pages.about_page as about_page
from nlapp.controller.AppController import (
    get_datasets_by_task_type,
    get_models_by_task_type,
    initialize_state,
)
from nlapp.data_model.state import KEYS
from nlapp.data_model.task_type import TaskType

PAGES = {
    "Evaluation": evaluation_page,
    "Statistics": statistics_page,
    "Train model": train_model_page,
    "About": about_page,
}


def write():
    initialize_state()

    sidebar.write(list(PAGES.keys()))

    current_page = st.session_state[KEYS.SELECTED_PAGE]
    PAGES[current_page].write()
