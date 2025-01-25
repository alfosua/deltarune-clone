import json


def load_json_resource(filename: str):
    with open(filename) as file:
        result = json.load(file)
        del result["$schema"]
        return result