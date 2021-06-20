import streamlit as st

from api.datasets.dataset_gateway import get_datasets_by_task_type

def dataset_print(dataset):
    name = dataset.name
    cached_info = "\u2713" if dataset.cached else "" 

    return f"{name} {cached_info}"

def write(task):
    st.header("Select dataset")

    datasets, _, description = st.beta_columns([6, 1, 5])

    with datasets:
        cached = st.checkbox("Cached only", key="datasetCached")
        dataset_dict = get_datasets_by_task_type(task)
        dataset_list = list(dataset_dict.values()) 
        dataset_list_filtered = list(filter(lambda dataset: not cached or dataset.cached, dataset_list))

        dataset = st.selectbox("Datasets", dataset_list_filtered, 
                format_func=dataset_print, help="In order to search just type while selecting") 

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

