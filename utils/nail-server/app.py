import PIL.Image
import numpy
import os
import io
import sys
import cv2
import requests
import base64
import tensorflow
import flask
from tensorflow.keras.applications.resnet import preprocess_input
from flask import Flask, json
from flask.json import jsonify

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import globals

globals.initialize()

app = Flask(__name__)

nail_model = dict()
nail_model['path'] = "nailFineTune[DenseNet121]Classifier.h5"

if not os.path.exists(nail_model['path']):
    os.system("gdown https://drive.google.com/uc\?id\=1w1bH_Phco63Kjj09ue-ORtZSBaX49a15")

nail_model['function'] = tensorflow.keras.models.load_model(nail_model['path'])

def decode(code=None):
    code = str.encode(code)
    code = base64.b64decode(code)
    code = io.BytesIO(code)
    image = PIL.Image.open(code)
    return(image)


def base2picture(resbase64):
    res = resbase64.split(',')[1]
    img_b64decode = base64.b64decode(res)
    image = io.BytesIO(img_b64decode)
    img = PIL.Image.open(image)
    img.save("test.jpg")
    return image


@app.route("/")
def describe():
    return "<b>Nail Server 運作中！</b>"


@app.route("/Nail-classifier", methods=["POST"])
def nail_classifier():
    # Receive request.
    data = flask.request.get_json(silent=True)
    size = (224, 224)

    if(data['format'] == 'url'):
        response = requests.get(data['image'])
        encoded_img = base64.b64encode(response.content)
        decoded_img = encoded_img.decode()
        image_uri = 'data:%s;base64,%s' % ('image/jpeg', decoded_img)
        img = base2picture(image_uri)
        image = PIL.Image.open(img)
        image = image.resize(size)
        image = numpy.expand_dims(numpy.array(image), axis=0)  # / 255

    if(data['format'] == 'path'):
        image = cv2.imread(data['image'])
        image = cv2.resize(image, size)
        image = numpy.expand_dims(numpy.array(image), axis=0)  # / 255

    if(data['format'] == 'base64'):
        image = decode(data['image']).resize(size)
        image = numpy.expand_dims(numpy.array(image), axis=0)  # / 255

    # image = preprocess_input(image)

    classification = {'atypical': 0, 'etc': 0, 'melanonychia': 0, 'naildystrophy': 0,
                      'nodule': 0, 'normalnail': 0, 'onycholysis': 0, 'onychomycosis': 0}
    score = [s for s in nail_model['function'].predict(
        image).squeeze(0).round(3)]
    likelihood = {k: str(v) for k, v in zip(classification, score)}
    key = max(likelihood, key=likelihood.get)
    prediction = {key: str(likelihood[key])}

    # Json response format.
    response = json.jsonify(
        {"likelihood": likelihood, "prediction": prediction})

    return(response)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=globals.config["port"]["Nail"],
        debug=False,
        threaded=False
    )