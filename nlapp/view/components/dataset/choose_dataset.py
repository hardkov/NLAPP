import streamlit as st
from nlapp.data_model.state import KEYS
import nlapp.view.components.dataset.huggingface_dataset as huggingface_dataset
import nlapp.view.components.dataset.user_dataset_upload as user_dataset_upload


def write():
    st.header("Select dataset")
    user_dataset_checkbox_placeholder, cached_checkbox_placeholder = st.columns(
        [3, 7]
    )

    with user_dataset_checkbox_placeholder:
        own_dataset = st.checkbox(
            "Upload your own dataset",
            key=KEYS.UPLOAD_USER_DATASET_TOGGLED,
            help="You can upload your own dataset after properly mapping it.",
        )

    if own_dataset:
        user_dataset_upload.write()

    else:
        huggingface_dataset.write(cached_checkbox_placeholder)
