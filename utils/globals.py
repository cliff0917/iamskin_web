import os
import json

def initialize():
    global config
    config = read_json(f'{os.path.dirname(os.path.abspath(__file__))}/config.json')

def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data