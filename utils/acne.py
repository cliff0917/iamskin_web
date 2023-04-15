import warnings

warnings.filterwarnings("ignore", category=Warning)

import os, sys, requests, torch, flask, PIL.Image
from flask import request, json

import globals
from mobile.process import save_img

# 找到 network 位置
root_path = os.getcwd()
sys.path.insert(0, root_path + "/utils")

from utils import bucket, network, acne_api

def get_post(server):
    service_type = 'Acne'
    api_config = bucket.loadYaml(path='./utils/acne_api.yaml')
    acne_api.downloadModels()
    models = acne_api.loadModel()

    @server.route(f"/{service_type}-classifier", methods=["POST"])
    def acne_classfier():
        # Receive request.
        format = request.form.get('format')
        upload_time = ''

        if format == 'upload':
            uid, upload_time, file_name, file_path = save_img(service_type)

        elif format == 'path':
            file_path = request.form.get('path')

        case = acne_api.createCase(path=file_path)
        predict_class, attr_prob = acne_api.inferCase(case, models, file_path)
        predict_class = 'low' if predict_class == 0 else 'high'
        output_url = f"https://{globals.config['domain_name']}/assets/{service_type}/img/{predict_class}.png"
        
        # Insert record to database
        if format == 'upload':
            info = (uid, service_type, upload_time, file_name, predict_class, -1, '', -1, '')
            database.add_history(info)

        # Json response format.
        response = json.jsonify(
            {
                "prediction": predict_class, 
                "prediction_chinese": globals.read_json(f"./assets/{service_type}/json/classes.json")[predict_class],
                "attr_prob": attr_prob,
                "upload_time": upload_time,
                "output_url": output_url
            }
        )
        return response

    return server