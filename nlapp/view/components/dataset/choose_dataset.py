import streamlit as st
from nlapp.data_model.state import KEYS
import nlapp.view.components.dataset.huggingface_dataset as huggingface_dataset
import nlapp.view.components.dataset.user_dataset_upload as user_dataset_upload


def write():
    own_dataset = st.checkbox(
        "Upload your own dataset",
        key=KEYS.UPLOAD_USER_DATASET_TOGGLED,
        help="You can upload your own dataset after properly mapping it."
    )
    header_placeholder = st.empty()

    if own_dataset:
        header_placeholder.header("Upload your dataset")

        user_dataset_upload.write()

    else:
        header_placeholder.header("Select dataset")

        huggingface_dataset.write()

