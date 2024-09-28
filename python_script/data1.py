import json


def getData():
    json_file = "combined_data.json"
    with open(json_file, "r") as json_file:
        data = json.load(json_file)
    return data
