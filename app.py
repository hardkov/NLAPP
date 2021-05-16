import streamlit as st

import components.model as model_component
import components.dataset as dataset_component
import components.sidebar as sidebar_component

apptitle = 'NLAPP'
st.set_page_config(page_title=apptitle, page_icon=":cat")


PAGES = { "Model": model_component, "Dataset": dataset_component }

def main():
  page_name = sidebar_component.write(PAGES)
  
  st.title("Common content for pages")

  page = PAGES[page_name]

  page.write()

if __name__ == "__main__":
  main()