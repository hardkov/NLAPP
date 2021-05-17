import streamlit as st

import components.choose_model as choose_model
import components.choose_dataset as choose_dataset
import components.sidebar as sidebar
import components.evaluation as evaluation
import components.choose_task as choose_task

apptitle = 'NLAPP'
st.set_page_config(page_title=apptitle, page_icon=":cat")

def main():
  sidebar.write()

  task = choose_task.write()
  model = choose_model.write(task)
  dataset = choose_dataset.write(task)

  evaluation.write(task, model, dataset)

if __name__ == "__main__":
  main()