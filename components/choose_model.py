import streamlit as st
import copy

def get_model_list(task, cached):
    if task == "Fill mask":
        base = [

            {
                "name": "bert-base-uncased", 
                "description": '''Pretrained model on English language using a masked language modeling (MLM) objective.
                    It was introduced in this paper and first released in this repository. This model is uncased: it
                    does not make a difference between english and English.''',
                "cached": True
            },
            {
                "name": "distilbert-baase-uncased", 
                "description": '''This model is a distilled version of the BERT base model.
                    It was introduced in this paper. The code for the distillation process can be found here.
                    This model is uncased: it does not make a difference between english and English.''',
                "cached": False
            }
        ] 
    else:
        base = [
            {
                "name": "distilbert-base-uncased-finetuned-sst-2-english", 
                "description": '''This model is a fine-tune checkpoint of DistilBERT-base-uncased,
                    fine-tuned on SST-2. This model reaches an accuracy of 91.3 on the dev set (for comparison,
                    Bert bert-base-uncased version reaches an accuracy of 92.7).''',
                "cached": False
            },
            {
                "name": "roberta-large-mnli", 
                "description": 'No description was provided',
                "cached": True
            }
        ] 

    return_list = []

    for i in range(5000):
        obj = copy.deepcopy(base[i % 2])
        obj["name"] += str(i)
        return_list.append(obj)

    return list(filter(lambda model: not cached or model["cached"], return_list))

def model_str(model):
    cached_info = "\u2713" if model["cached"] else "" 

    return f"{model['name']} {cached_info}"

def write(task):
    st.header("Select model")

    models, _, description = st.beta_columns([6, 1, 5])

    with models:
        cached = st.checkbox("Cached only", key="modelCached")
        model_list = get_model_list(task, cached)
        model = st.selectbox("Models", model_list, format_func=model_str, help="In order to search just type while selecting") 

    # description in markdown with links
    with description:
        st.subheader("Model description")
        if model is not None:
            st.write(model["description"])

            if model["cached"]:
                st.success("Model is stored on the disk")
            else:
                st.warning("Model needs to be downloaded")

    return model

