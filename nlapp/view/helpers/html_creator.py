import json
from math import ceil


def get_result_html(result_divs):
    return f"""
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <style type="text/css">
        .progress {{
            background: rgb(255, 255, 255);
        }}
        .progress-bar {{
            background: rgb(246,51,102);
            background: linear-gradient(90deg, rgba(246,51,102,1) 35%, rgba(255,255,255,1) 110%);    
        }}
    </style>
    <div class="container-fluid m-0">
        {result_divs}
    </div>
    """


def get_token_div(result):
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


def get_html_from_result_json(result_json):
    results = json.loads(result_json)
    result_divs = []
    for result in results:
        result_divs.append(get_token_div(result))
    return get_result_html("\n".join(result_divs)), 300
