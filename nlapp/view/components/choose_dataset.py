import streamlit as st
from nlapp.controller.AppController import get_datasets_by_task_type
from nlapp.data_model.state import KEYS


def dataset_print(dataset):
    name = dataset.name
    cached_info = "\u2713" if dataset.cached else ""

    return f"{name} {cached_info}"


def write():
    task = st.session_state[KEYS.SELECTED_TASK]

    st.header("Select dataset")

    datasets, _, description = st.columns([6, 1, 5])

    with datasets:
        cached = st.checkbox("Cached only", key=KEYS.IS_DATASET_CACHED)
        dataset_dict = get_datasets_by_task_type(task)
        dataset_list = list(dataset_dict.values())
        dataset_list_filtered = list(
            filter(lambda dataset: not cached or dataset.cached, dataset_list)
        )

        dataset = st.selectbox(
            "Datasets",
            dataset_list_filtered,
            key=KEYS.SELECTED_DATASET,
            format_func=dataset_print,
            help="In order to search just type while selecting",
        )

    # description in markdown with links
    with description:
        st.subheader("Dataset description")
        if dataset is not None:
            st.markdown(dataset.description)

            if dataset.cached:
                st.success("Dataset is stored on the disk")
            else:
                st.warning("Dataset needs to be downloaded")

    return dataset
