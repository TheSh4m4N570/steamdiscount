from selectolax.parser import Node
from datetime import datetime
import pandas as pd
import re

def get_attrs_from_node(node: Node, attr: str):
    if node is None or not issubclass(Node, type(node)):
        raise ValueError("The function excepts a selectolax node to be provided")
    return node.attrs.get(attr)


def get_first_n(input_list: list, n: int = 5):
    return input_list[:n]


def reformat_date(date_raw: str, from_format: str, to_format: str):
    dt_obj = datetime.strptime(date_raw, from_format)
    return datetime.strftime(dt_obj, to_format)

def regex(input_str: str, pattern: str):
    return re.findall(pattern, input_str)

def format_and_transform(attrs: dict):
    transforms = {
        "thumbnail": lambda n: get_attrs_from_node(n, 'src'),
        "tags": lambda input_list: get_first_n(input_list, 5),
        "release_date": lambda date: reformat_date(date, "%b %d, %Y", "%Y-%m-%d"),
        "reviews": lambda raw: int(''.join(regex(raw, r'\d+')))
    }

    for k, v in transforms.items():
        if k in attrs:
            attrs[k] = v(attrs[k])

    return attrs


def save_to_file(filename="extract.csv", data: list[dict]= None):
    if data is None:
        raise ValueError("The function excpects data to be provided as a list of dictionaries")
    df = pd.DataFrame(data)
    filename = f"{datetime.now().strftime('%Y_%m_%d')}_{filename}.csv"
    df.to_csv(filename, index=False)