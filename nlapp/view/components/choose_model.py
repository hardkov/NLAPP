import streamlit as st
from nlapp.controller.AppController import get_models_names, get_model_dto
from nlapp.data_model.state import KEYS


def write():
    task = st.session_state[KEYS.SELECTED_TASK]

    st.header("Select model")

    models, _, description = st.columns([6, 1, 5])

    with models:
        cached = st.checkbox("Cached only", key=KEYS.IS_MODEL_CACHED)
        model_names = get_models_names(task, cached)

        model_name = st.selectbox(
            "Models",
            model_names,
            key=KEYS.SELECTED_MODEL,
            help="In order to search just type while selecting",
        )

    model_dto = get_model_dto(task, model_name)

    with description:
        st.subheader("Model description")
        st.markdown(model_dto.description)

        if model_dto.cached:
            st.success("Model is stored on the disk")
        else:
            st.warning("Model needs to be downloaded")
