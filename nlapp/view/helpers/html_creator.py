import json
from math import ceil
from typing import List
import random

from data_model.token_classification.token_classification_part_result import TokenClassificationPartResult

progress_bar_css = """
<style type="text/css">
    .progress {
        background: rgb(255, 255, 255);
    }
    .progress-bar {
        background: rgb(246,51,102);
        background: linear-gradient(90deg, rgba(246,51,102,1) 35%, rgba(255,255,255,1) 110%);    
    }
</style>
"""

badge_css = """
<style type="text/css">
    
    .outer {
        color: white;
        font-size: 90%;
    }
      
    .inside {   
        color: white;
        font-size: 75%;
    }
      
    .blue {
        background-color: #6694c5;
    }
      
    .blue .inside {
        background-color: #0d58a9;
    }
      
    .red {
        background-color: #ff4b4b;
    }
      
    .red .inside {
        background-color: #c11d1d;
    }
    
    .orange {
        background-color: #e9bb5c;
    }
      
    .orange .inside {
        background-color: #cb8e13;
    }
    
    .green {
        background-color: #3ed939;
    }
      
    .green .inside {
        background-color: #11b30c;
    }
    
      
</style>
"""


def get_result_html(own_css, body):
    return f"""
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">

    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

    <!-- Popper JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script> 
    {own_css}
    <div class="container-fluid m-0">
        {body}
    </div>
    <script>
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {{
        return new bootstrap.Tooltip(tooltipTriggerEl)
    }})
    console.log(tooltipTriggerList);
    </script>
    """


def get_result_bar(result):
    value = result["score"]
    if value > 1 or value < 0:
        raise ValueError("score has to be between 0 and 1")
    width = ceil(value * 100)
    percent = ceil(value * 1000) / 1000
    token = result["token_str"]
    return f"""
    <div class="d-flex flex-row my-2 align-items-center">
        <div class="col-10">
            <div class="progress">
                <div class="progress-bar" role="progressbar" style="width: {width}%"></div>
            </div>
            <p class="m-0 text-monospace">{token}</p>
        </div>
        <div class="col-2">
            <p class="m-0 text-monospace text-right ">{percent}</p>
        </div>
    </div>
    """


def token_classification_badge(word, classification, score, color_class):
    return f'''
    <span data-toggle="tooltip" data-html="true" title="<b>Score</b> : {score}"
    class="badge outer {color_class}">{word} <span class="badge inside {color_class}"> {classification}</span></span>
'''


def get_random_color_class():
    color_classes = {
        0: "red",
        1: "blue",
        2: "orange",
        3: "green"
    }
    return color_classes[random.randint(0, 3)]

def replace_word_with_badge(sentence: str, result: TokenClassificationPartResult):
    start = result.start
    end = result.end
    word = sentence[start:end]
    entity = remove_entity_prefixes(result.entity)
    score = round(result.score, 10)
    color_class = get_random_color_class()
    return sentence[:start] + token_classification_badge(word, entity, score, color_class) + sentence[end:]


def remove_entity_prefixes(entity: str):
    return entity.removeprefix("I-").removeprefix("B-")


def get_html_from_result_json(result_json):
    results = json.loads(result_json)
    result_bars = []
    for result in results:
        result_bars.append(get_result_bar(result))
    return get_result_html(progress_bar_css, "\n".join(result_bars)), 300


def get_token_classification_evaluation_html(sentence: str, results: List[TokenClassificationPartResult]):
    body = sentence
    for result in reversed(results):
        print(result)
        body = replace_word_with_badge(body, result)
    return get_result_html(badge_css, body), 100


