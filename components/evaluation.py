import streamlit as st

import json
from api.evaluation.fill_mask_evaluation import evaluate_sentence, evaluate_dataset
from api.task_type import TaskType
from components.helpers import html_creator
from api.models.model_gateway import download_model
from api.datasets.dataset_gateway import download_dataset


def parse_result_to_json(result):
  token_score_list = list()
  for token_score in result.tokens_score:
    json_dict = dict()
    json_dict['token_str'] = token_score.token
    json_dict['score'] = token_score.score
    token_score_list.append(json_dict)
  return json.dumps(token_score_list)


def evaluate(model, tokenizer, value):
  result = evaluate_sentence(value, model, tokenizer)
  return parse_result_to_json(result)


@st.cache(hash_funcs={"tokenizers.Tokenizer": id, "tokenizers.AddedToken": id}, max_entries=1)
def download_model_with_cache(task, model_name):
  return download_model(task, model_name)

@st.cache(hash_funcs={"pyarrow.lib.Buffer": id}, allow_output_mutation=True, max_entries=1)
def download_dataset_with_cache(task, dataset):
    return download_dataset(task, dataset.name)

@st.cache(hash_funcs={"pyarrow.lib.Buffer": id, "tokenizers.Tokenizer": id, "tokenizers.AddedToken": id})
def evaluate_dataset_with_cache(dataset, model, tokenizer, timeout_seconds):
  return evaluate_dataset(dataset, model, tokenizer, timeout_seconds)

def write(task, model, dataset):
  st.header("Results")

  should_download_model = st.checkbox("Toggle model fetching")

  if should_download_model:
    st.subheader("Manual input")

    model, tokenizer = download_model_with_cache(task, model.name)

    form = st.form(key='my-form')
    value = form.text_input(task.name, value="Warsaw is the [MASK] of Poland.")
    form.form_submit_button('Evaluate')

    result_json = evaluate(model, tokenizer, value)
    html_code, height = html_creator.get_html_from_result_json(result_json)
    st.components.v1.html(html_code, height=height)

    st.subheader("Dataset input")
    dataset_input_enabled = st.button("Download & Compute", key="dataset_input_enabled")

    if dataset_input_enabled:
      dataset = download_dataset_with_cache(task, dataset)
      results = evaluate_dataset_with_cache(dataset, model, tokenizer, timeout_seconds=10)
      st.write(results)

