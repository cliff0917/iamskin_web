import PIL.Image
import numpy as np
import cv2, requests, base64, flask
from flask import json
from tensorflow.keras.models import load_model

from utils.transfer import decode, base2picture

def get_post(server):
    model = load_model('./models/Skin.h5')

    @server.route("/Skin-classifier", methods=["POST"])
    def skin_classfier():
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
            image = np.expand_dims(np.array(image), axis=0) # / 255

        if(data['format'] == 'path'):
            image = cv2.imread(data['image'])
            image = cv2.resize(image, size)
            image = np.expand_dims(np.array(image), axis=0) # / 255

        if(data['format'] == 'base64'):
            image = decode(data['image']).resize(size)
            image = np.expand_dims(np.array(image), axis=0)  # / 255

        # Prediction summary.
        classification = {"dry": 0.0, "oily": 0.0, "sensitive": 0.0}
        score = [s for s in model.predict(image).squeeze(0).round(3)]
        likelihood = {k: str(v) for k, v in zip(classification, score)}
        key = max(likelihood, key=likelihood.get)
        prediction = {key: str(likelihood[key])}

        # Json response format.
        response = json.jsonify(
            {"likelihood": likelihood, "prediction": prediction}
        )
        return response
        
    return server