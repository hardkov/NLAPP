import streamlit as st
from nlapp.controller.AppController import get_models_by_task_type, fetch_description
from nlapp.data_model.state import KEYS


def model_print(model):
    name = model.name
    cached_info = "\u2713" if model.cached else ""

    return f"{name} {cached_info}"


def write():
    task = st.session_state[KEYS.SELECTED_TASK]

    st.header("Select model")

    models, _, description = st.columns([6, 1, 5])

    with models:
        cached = st.checkbox("Cached only", key=KEYS.IS_MODEL_CACHED)
        model_dict = get_models_by_task_type(task)
        model_list = list(model_dict.values())
        model_list_filtered = list(
            filter(lambda model: not cached or model.cached, model_list)
        )

        model = st.selectbox(
            "Models",
            model_list_filtered,
            key=KEYS.SELECTED_MODEL,
            format_func=model_print,
            help="In order to search just type while selecting",
        )

    # description in markdown with links
    with description:
        st.subheader("Model description")
        if model is not None:
            if description != "":
                fetch_description(model.name)
            st.markdown(model.description)

            if model.cached:
                st.success("Model is stored on the disk")
            else:
                st.warning("Model needs to be downloaded")
