import streamlit as st

import nlapp.view.components.choose_model as choose_model
import nlapp.view.components.choose_dataset as choose_dataset
import nlapp.view.components.evaluation as evaluation
import nlapp.view.components.choose_task as choose_task


def write():
    st.title("Evaluation")

    task = choose_task.write()
    model = choose_model.write(task)
    dataset = choose_dataset.write(task)

    evaluation.write(task, model, dataset)
