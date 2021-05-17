from components.choose_model import get_model_list
import streamlit as st

def get_dataset_list(task, search, cached):
    # do some fancy stuff, call api...
    if task == "Fill mask":
        return ["acronym_identification", "aeslc"]

    return ["ade_corpus_v2", "ajgt_twitter_ar Copied"]

def write(task):
    st.title("This is choose_dataset")

    search = st.text_input("Search", key="datasetSearch")
    cached = st.checkbox("Cached only", key="datasetCached")

    dataset_list = get_dataset_list(task, search, cached)
    dataset = st.selectbox("Dataset", dataset_list)

    return dataset