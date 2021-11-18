import streamlit as st

from nlapp.controller.app_controller import get_datasets_names, get_dataset_dto, get_current_task
from nlapp.data_model.state import KEYS


def write(placeholder):
    task = get_current_task()

    datasets, _, description = st.columns([6, 1, 5])

    with placeholder:
        cached = st.checkbox("Cached only", key=KEYS.IS_DATASET_CACHED)

    with datasets:
        datasets_names = get_datasets_names(task, cached)

        dataset_name = st.selectbox(
            "Datasets",
            datasets_names,
            key=KEYS.SELECTED_DATASET,
            help="In order to search just type while selecting",
        )

    if dataset_name is None:
        return

    dataset_dto = get_dataset_dto(task, dataset_name)

    with description:
        st.subheader("Dataset description")
        st.markdown(dataset_dto.description)

        if dataset_dto.cached:
            st.success("Dataset is stored on the disk")
        else:
            st.warning("Dataset needs to be downloaded")
