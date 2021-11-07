import streamlit as st

import nlapp.view.components.dataset.choose_dataset as choose_dataset
import nlapp.view.components.choose_model as choose_model
import nlapp.view.components.choose_task as choose_task
import nlapp.view.components.evaluation as evaluation


def write():
    st.title("Evaluation")

    choose_task.write()
    choose_model.write()
    choose_dataset.write()

    evaluation.write()
