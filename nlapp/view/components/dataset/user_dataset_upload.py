import streamlit as st
import json
from io import StringIO

from nlapp.data_model.state import KEYS
from nlapp.controller.app_controller import (
    load_user_dataset,
    get_dataset_mapping_columns
)
from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.service.datasets.dataset_gateway import __user_dataset_mapper_factory

def check_mapping_value_are_not_empty(column_mapping):
    return all([val is not None and val != "" for val in column_mapping.values()])

def get_json_string(file):
    stringio = StringIO(file.getvalue().decode("utf-8"))
    return stringio.read()

def write():
    task = st.session_state[KEYS.SELECTED_TASK]

    _ = st.file_uploader("Allowed extensions: .json", type=["json"], key=KEYS.USER_DATASET_FILE)
    user_file = st.session_state[KEYS.USER_DATASET_FILE]
    if user_file is not None:
        st.subheader("Map your dataset")

        json_string = get_json_string(user_file)
        st.json(json_string)

        column_mapping = {}
        columns = get_dataset_mapping_columns(task)

        mapping_form = st.form("Mapping")
        mapping_form.subheader("Mapping")
        for column in columns:
            mapping_form.markdown(f"Enter your mapping for **{column}** field")
            column_mapping[column] = mapping_form.text_input("Your mapping",
                                                   key=column)
        submitted = mapping_form.form_submit_button("Map")
        if submitted:
            if check_mapping_value_are_not_empty(column_mapping):
                try:
                    mapped = load_user_dataset(
                        task_type=task,
                        column_mapping=column_mapping,
                        file_type=DatasetFormat.JSON,
                        dataset=json.loads(json_string)
                    )
                except Exception as ex:
                    print(ex)
                    st.session_state[KEYS.MAPPED_USER_DATASET] = None
                    st.warning("Wrong mapping!")
                else:
                    print(mapped)
                    st.session_state[KEYS.MAPPED_USER_DATASET] = mapped
            else:
                st.error("You have to fill all fields!")
