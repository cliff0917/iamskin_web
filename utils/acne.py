import warnings

warnings.filterwarnings("ignore", category=Warning)

import os, sys, requests, base64, torch, flask, PIL.Image
from flask import json

# 找到 network 位置
root_path = os.getcwd()
sys.path.insert(0, root_path + "/utils")

from utils import bucket, network, acne_api

def get_post(server):
    api_config = bucket.loadYaml(path='./utils/acne_api.yaml')
    acne_api.downloadModels()
    models = acne_api.loadModel()

    @server.route("/Acne-classifier", methods=["POST"])
    def acne_classfier():
        # Receive request.
        data = flask.request.get_json(silent=True)

        # website
        if data['format'] == 'path':
            img_path = data['image']

        # linebot
        else:
            img_path = data['image']

        case = acne_api.createCase(path=img_path)
        predict_class, attr_prob = acne_api.inferCase(case, models, img_path)
        prediction = 'low' if predict_class == 0 else 'high'

        # Json response format.
        response = json.jsonify(
            {"prediction": prediction, "attr_prob": attr_prob}
        )
        return response

    return server