import streamlit as st

import nlapp.components.choose_model as choose_model
import nlapp.components.choose_dataset as choose_dataset
import nlapp.components.evaluation as evaluation
import nlapp.components.choose_task as choose_task


def write():
    st.title("Evaluation")

    task = choose_task.write()
    model = choose_model.write(task)
    dataset = choose_dataset.write(task)

    evaluation.write(task, model, dataset)
