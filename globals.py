import os
import json
from datetime import datetime

from lib import database

def initialize():
    global config, services, rate_text
    config = read_json('./config.json')
    database.create_db()
    services = [f'/{service}' for service in config['chinese'].keys()]
    rate_text = ['不好用', '有待改進', '還可以', '不錯用', '非常棒']

def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def now():
    time_format = "%Y-%m-%d@%H:%M:%S"
    return datetime.now().strftime(time_format)