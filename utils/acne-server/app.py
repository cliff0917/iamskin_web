import warnings

warnings.filterwarnings("ignore", category=Warning)

import io
import os
import sys
import torch
import flask
import PIL.Image
import requests
import base64
from flask import Flask, json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import globals, bucket, network, api


globals.initialize()

api_config = bucket.loadYaml(path='./api.yaml')
api.downloadModels()
models = api.loadModel()

app = Flask(__name__)

def base2picture(resbase64):
    res = resbase64.split(',')[1]
    img_b64decode = base64.b64decode(res)
    image = io.BytesIO(img_b64decode)
    img = PIL.Image.open(image)
    return image


@app.route("/")
def describe():
    return "<b>Acne Server 運作中！</b>"


@app.route("/Acne-classifier", methods=["POST"])
def acne_classfier():
    # Receive request.
    data = flask.request.get_json(silent=True)

    # website
    if data['format'] == 'path':
        img_path = data['image']

    # linebot
    else:
        img_path = f"../linebot/{data['image']}"

    case = api.createCase(path=img_path)
    predict_class, attr_prob = api.inferCase(case, models, img_path)
    prediction = 'low' if predict_class == 0 else 'high'

    # Json response format.
    response = json.jsonify(
        {"prediction": prediction, "attr_prob": attr_prob}
    )
    return(response)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=globals.config["port"]["Acne"],
        debug=False,
        threaded=False
    )