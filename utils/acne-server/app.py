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

import globals

globals.initialize()

if not os.path.exists('best.pt'):
    os.system("gdown https://drive.google.com/uc\?id\=1rMAGNvnXoY9Q_mtuZ_Kzf3xLucX3jXdB")

app = Flask(__name__)

model_name = 'yolov5x'
model_weight = "best.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_weight)

def base2picture(resbase64):
    res = resbase64.split(',')[1]
    img_b64decode = base64.b64decode(res)
    image = io.BytesIO(img_b64decode)
    img = PIL.Image.open(image)
    img.save("test.jpg")
    return image


def get_severity(num):
    if num in range(0, 5):
        severity = 'low' # Mild
    elif num in range(5, 21):
        severity = 'middle' # Moderate
    elif num in range(21, 41):
        severity = 'm_high' # Severe
    else:
        severity = 'high' # Very-Severe
    return severity


@app.route("/")
def describe():
    return "<b>Acne Server 運作中！</b>"


@app.route("/Acne-classifier", methods=["POST"])
def acne_classfier():
    # Receive request.
    data = flask.request.get_json(silent=True)
    # print(data)

    if(data['format'] == 'url'):
        response = requests.get(data['image'])
        encoded_img = base64.b64encode(response.content)
        decoded_img = encoded_img.decode()
        image_uri = 'data:%s;base64,%s' % ('image/jpeg', decoded_img)
        img = base2picture(image_uri)
        image = PIL.Image.open(img)
        image_path = image
        image_prediction = model(image_path).pandas().xyxy[0]

    if(data['format'] == 'path'):
        image_path = data['image']
        image_prediction = model(image_path).pandas().xyxy[0]

    # Prediction summary.
    count = len(image_prediction)
    # print("count:{}".format(count))
    prediction = get_severity(count)

    # Json response format.
    response = json.jsonify(
        {"count": count, "prediction": prediction})
    return(response)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=globals.config["port"]["Acne"],
        debug=False,
        threaded=False
    )