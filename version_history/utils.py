import json
import ast


def string_to_json(json_data):
    json_data = ast.literal_eval(json_data)
    return json.dumps(json_data)


def json_to_string(string_data):
    return json.loads(string_data)