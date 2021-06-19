import streamlit as st

import json
from api.evaluation.fill_mask_evaluation import evaluate_sentence
from api.task_type import TaskType
from components.helpers import html_creator


def parse_result_to_json(result):
  token_score_list = list()
  for token_score in result.tokens_score:
    json_dict = dict()
    json_dict['token_str'] = token_score.token
    json_dict['score'] = token_score.score
    token_score_list.append(json_dict)
  return json.dumps(token_score_list)


def evaluate(model, dataset, value):
  result = evaluate_sentence(sentence=value, model=model.name, task_type=TaskType.FILL_MASK)
  return parse_result_to_json(result)


def write(task, model, dataset):
  if task == TaskType.FILL_MASK.name:
    st.title(f"Evaluating of task {task.lower().replace('_',' ')}")
    form = st.form(key='my-form')
    value = form.text_input(task, value="Warsaw is the [MASK] of Poland.")
    submit = form.form_submit_button('Evaluate')

    if not submit:
      st.write('Press evaluate to get results')
    else:
      result_json = evaluate(model, dataset, value)
      html_code, height = html_creator.get_html_from_result_json(result_json)
      st.components.v1.html(html_code, height=height)
