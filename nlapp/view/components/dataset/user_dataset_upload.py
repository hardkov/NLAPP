import streamlit as st
import json
from io import StringIO

from data_model.task_type import TaskType
from nlapp.data_model.state import KEYS
from nlapp.controller.app_controller import (
    load_user_dataset,
    get_dataset_mapping_columns,
    get_current_task,
)
from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.view.helpers import conllu_panda_mapper as mapper


def check_mapping_value_are_not_empty(column_mapping):
    return all(
        [val is not None and val != "" for val in column_mapping.values()]
    )


def get_json_string(file):
    stringio = StringIO(file.getvalue().decode("utf-8"))
    return stringio.read()


def display_json_mapper(user_file):
    task = get_current_task()
    st.subheader("Map your dataset")

    json_string = get_json_string(user_file)
    st.json(json_string)

    column_mapping = {}
    columns = get_dataset_mapping_columns(task)

    mapping_form = st.form("Mapping")
    mapping_form.subheader("Mapping")
    for column in columns:
        mapping_form.markdown(f"Enter your mapping for **{column}** field")
        column_mapping[column] = mapping_form.text_input(
            "Your mapping", key=column
        )
    submitted = mapping_form.form_submit_button("Map")
    if submitted:
        if check_mapping_value_are_not_empty(column_mapping):
            try:
                mapped = load_user_dataset(
                    task_type=task,
                    column_mapping=column_mapping,
                    file_type=DatasetFormat.JSON,
                    dataset=json.loads(json_string),
                )
            except Exception as ex:
                st.session_state[KEYS.MAPPED_USER_DATASET] = None
                st.warning("Wrong mapping!")
            else:
                st.session_state[KEYS.MAPPED_USER_DATASET] = mapped
                st.success("Mapped successfully.")
        else:
            st.error("You have to fill all fields!")


def display_conllu_mapper(user_file):
    df = mapper.map_conllu_df(get_json_string(user_file))
    st.dataframe(df, height=500)


def display_mapper(user_file):
    is_json = not st.session_state[KEYS.IS_USER_FILE_CONLLU]
    if is_json:
        display_json_mapper(user_file)
    else:
        display_conllu_mapper(user_file)


def display_file_view(extension, file_key):
    file_uploader_description = f"Allowed extensions: .{extension}"
    st.session_state[KEYS.IS_USER_FILE_CONLLU] = extension != "json"

    user_file = st.file_uploader(
        file_uploader_description,
        type=[f"{extension}"],
        key=file_key,
        accept_multiple_files=False,
    )
    if user_file is not None:
        display_mapper(user_file)


def write():
    task = get_current_task()

    st.subheader("Upload file")
    if task.value is TaskType.TOKEN_CLASSIFICATION.value:
        conllu_file = st.checkbox("Conllu files")

        if conllu_file:
            display_file_view("conllu", KEYS.CONLLU_USER_DATASET_FILE)
        else:
            display_file_view("json", KEYS.JSON_USER_DATASET_FILE)

    else:
        display_file_view("json", KEYS.JSON_USER_DATASET_FILE)
