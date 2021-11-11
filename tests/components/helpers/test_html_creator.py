import pytest
from nlapp.view.helpers.html_creator import *


def expected_token_div(expected_width, expected_token_str, expected_percent):
    return f"""
    <div class="d-flex flex-row my-2 align-items-center">
        <div class="col-10">
            <div class="progress">
                <div class="progress-bar" role="progressbar" style="width: {expected_width}%"></div>
            </div>
            <p class="m-0 text-monospace">{expected_token_str}</p>
        </div>
        <div class="col-2">
            <p class="m-0 text-monospace text-right ">{expected_percent}</p>
        </div>
    </div>
    """


def expected_html(value):
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
        {value}
    </div>
    """


def test_get_token_div():
    test_score_value = 0.5653
    test_token_str_value = "test_word"
    test_dict = {"score": test_score_value, "token_str": test_token_str_value}

    expected_width = 57
    expected_percent = 0.566
    expected = expected_token_div(
        expected_width, test_token_str_value, expected_percent
    )

    assert get_token_div(test_dict) == expected


@pytest.mark.parametrize(
    "expected_score_value,expected_width,expected_token_str,expected_percent",
    [
        (0.12223123, 13, "test1", 0.123),
        (0.23624662, 24, "tests", 0.237),
        (0.96960034, 97, "tests", 0.97),
    ],
)
def test_parametrized_get_token_div(
    expected_score_value, expected_width, expected_token_str, expected_percent
):
    test_dict = {"score": expected_score_value, "token_str": expected_token_str}

    expected = expected_token_div(
        expected_width, expected_token_str, expected_percent
    )

    assert get_token_div(test_dict) == expected


def test_get_token_div_should_raise_error_when_wrong_score():
    test_score_value = 1.11223123
    test_token_str_value = "test_word"
    test_dict = {"score": test_score_value, "token_str": test_token_str_value}

    with pytest.raises(ValueError) as e:
        get_token_div(test_dict)
    assert "score has to be between 0 and 1" in str(e.value)


def test_get_result_html():
    test_val = "<div></div>\n<div></div>"
    expected = expected_html(test_val)
    assert get_result_html(test_val) == expected
