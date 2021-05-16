import streamlit as st

from pages.model import model_page
from pages.dataset import dataset_page

apptitle = 'NLAPP'
st.set_page_config(page_title=apptitle, page_icon=":cat")


PAGES = { "Model": model_page, "Dataset": dataset_page }

def main():
  page_name = st.sidebar.radio("Choose page", list(PAGES.keys()))
  
  st.title("Common content for pages")

  page = PAGES[page_name]

  page()

if __name__ == "__main__":
  main()