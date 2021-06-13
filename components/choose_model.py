from api.models.model_gateway import get_models_by_task_type
from api.task_type import TaskType
import streamlit as st

def model_str(model):
    name = model.name
    cached_info = "\u2713" if model.cached else "" 

    return f"{name} {cached_info}"

def write(task):
    st.header("Select model")

    models, _, description = st.beta_columns([6, 1, 5])

    with models:
        cached = st.checkbox("Cached only", key="modelCached")
        model_dict = get_models_by_task_type(TaskType[task])
        model_list = list(model_dict.values())
        model_list_filtered = list(filter(lambda model: not cached or model.cached, model_list))
        model = st.selectbox("Models", model_list_filtered, 
                format_func=model_str, help="In order to search just type while selecting") 

    # description in markdown with links
    with description:
        st.subheader("Model description")
        if model is not None:
            st.markdown(model.description)

            if model.cached:
                st.success("Model is stored on the disk")
            else:
                st.warning("Model needs to be downloaded")

    return model

