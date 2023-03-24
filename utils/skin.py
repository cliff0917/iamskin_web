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
        likelihood = {k: float(v) for k, v in zip(classification, score)}
        predict_class = max(likelihood, key=likelihood.get)

        # Json response format.
        response = json.jsonify(
            {"likelihood": likelihood, "prediction": predict_class}
        )
        return response
        
    return server