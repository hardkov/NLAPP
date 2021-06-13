import streamlit as st

from api.datasets.task_type import TaskType
from components.helpers import html_creator


def evaluate(model, dataset, value):
  print(value)
  with open('./components/helpers/example_result.json', 'r') as file:
    return file.read()


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
