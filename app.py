import streamlit as st

import components.model as model_component
import components.dataset as dataset_component
import components.sidebar as sidebar_component
import components.menu as menu_component

apptitle = 'NLAPP'
st.set_page_config(page_title=apptitle, page_icon=":cat")

# state: task, model, dataset

PAGES = { "Menu": menu_component, "Model": model_component, "Dataset": dataset_component }

def main():
  page_name = sidebar_component.write(PAGES)
  page = PAGES[page_name]
  page.write()

if __name__ == "__main__":
  main()