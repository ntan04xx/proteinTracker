#!/bin/python3

import json

data_path = 'data.json'

def get_data():
    with open(data_path, "r") as f:
        return json.load(f)

def set_data(newData):
    with open(data_path, "w") as f:
        json.dump(newData, f)
