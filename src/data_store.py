#!/bin/python3

import json

data_path = 'data.json'

def get_data():
    with open(data_path, "r") as f:
        return json.load(f)

def new_profile(new_profile):
    data = get_data()
    data["users"].append(new_profile)
    with open(data_path, "w") as f:
        json.dump(data, f)

def clean_data():
    original_data = {"users": []}
    with open(data_path, "w") as f:
        json.dump(original_data, f)
