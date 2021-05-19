import streamlit as st
import copy

def get_dataset_list(task, cached):
    if task == "Fill mask":
        base = [
            {
                "name": "acronym_identification", 
                "description": '''This dataset contains the training, validation, and test data for the
                                Shared Task 1: Acronym Identification of the AAAI-21 Workshop on 
                                Scientific Document Understanding.''',
                "cached": True
            },
            {
                "name": "aeslc", 
                "description": '''A collection of email messages of employees in the Enron Corporation.
                            There are two features:
                            email_body: email body text.
                            subject_line: email subject text.''',
                "cached": False
            }
        ] 
    else:
        base = [
            {
                "name": "ade_corpus_v2", 
                "description": '''ADE-Corpus-V2 Dataset: Adverse Drug Reaction Data. This is a dataset for Classification if a
                                sentence is ADE-related (True) or not (False) and Relation Extraction between Adverse Drug Event and Drug.
                                DRUG-AE.rel provides relations between drugs and adverse effects. DRUG-DOSE.rel provides 
                                relations between drugs and dosages. ADE-NEG.txt provides all sentences in the ADE corpus that 
                                DO NOT contain any drug-related adverse effects.''',

                "cached": False
            },
            {
                "name": "ajgt_twitter_ar", 
                "description": '''Arabic Jordanian General Tweets (AJGT) Corpus consisted of 1,800 tweets annotated as
                                positive and negative. Modern Standard Arabic (MSA) or Jordanian dialect.''',
                "cached": True
            }
        ] 

    return_list = []

    for i in range(5000):
        obj = copy.deepcopy(base[i % 2])
        obj["name"] += str(i)
        return_list.append(obj)

    return list(filter(lambda dataset: not cached or dataset["cached"], return_list))

def dataset_str(dataset):
    cached_info = "\u2713" if dataset["cached"] else "" 

    return f"{dataset['name']} {cached_info}"

def write(task):
    st.header("Select dataset")

    datasets, _, description = st.beta_columns([6, 1, 5])

    with datasets:
        cached = st.checkbox("Cached only", key="datasetCached")
        dataset_list = get_dataset_list(task, cached)
        dataset = st.selectbox("Datasets", dataset_list, format_func=dataset_str, help="In order to search just type while selecting") 

    # description in markdown with links
    with description:
        st.subheader("Dataset description")
        if dataset is not None:
            st.write(dataset["description"])

            if dataset["cached"]:
                st.success("Dataset is stored on the disk")
            else:
                st.warning("Dataset needs to be downloaded")

    return dataset

