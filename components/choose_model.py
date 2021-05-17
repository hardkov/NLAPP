import streamlit as st


def get_model_list(task, search, cached):
    # do some fancy stuff, call api...
    if task == "Fill mask":
        return ["bert-base-uncased", "distilbert-baase-uncased"]

    return ["distilbert-base-uncased-finetuned-sst-2-english", "roberta-large-mnli"]

def write(task):
    st.title("This is choose_model")

    search = st.text_input("Search", key="modelSearch")
    cached = st.checkbox("Cached only", key="modelCached")

    model_list = get_model_list(task, search, cached)
    model = st.selectbox("Model", model_list)

    return model

