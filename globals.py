import os
import json

def initialize():
    global config
    config = read_json('./config.json')

def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def build_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)