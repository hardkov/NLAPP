import requests

from bs4 import BeautifulSoup
from api.task_type import TaskType


def prepare_datasets_csv():
    datasets = dict()

    for task_type in TaskType:
        datasets[task_type] = find_datasets_by_task(task_type)


def find_datasets_by_task(task_type: TaskType):
    datasets = list()
    header_class = 'text-sm md:text-base font-mono group-hover:text-red-500'

    page_url = 'https://huggingface.co/datasets?filter={filter}'.format(filter=task_type.get_dataset_filter())
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for header in soup.findAll('h4', {"class": header_class}):
        print(header.getText())
        datasets.append(header.getText())

    return datasets





