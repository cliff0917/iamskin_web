import PIL.Image
import numpy as np
import os, cv2
from flask import request, json
from tensorflow.keras.models import load_model

import globals
from mobile.process import save_img, build_link

def get_post(server):
    model = load_model('./models/Nail.h5')

    @server.route("/Nail-classifier", methods=["POST"])
    def nail_classifier():
        # Receive request.
        format = request.form.get('format')
        size = (224, 224)

        if format == 'upload':
            uid, upload_time, file_name, file_path = save_img('Nail')

        elif format == 'path':
            file_path = request.form.get('path')

        image = cv2.imread(file_path)
        image = cv2.resize(image, size)
        image = np.expand_dims(np.array(image), axis=0) # / 255

        classification = {'atypical': 0, 'etc': 0, 'melanonychia': 0, 'naildystrophy': 0,
                        'nodule': 0, 'normalNail': 0, 'onycholysis': 0, 'onychomycosis': 0}
        score = [s for s in model.predict(image).squeeze(0).round(3)]
        likelihood = {k: str(v) for k, v in zip(classification, score)}
        predict_class = max(likelihood, key=likelihood.get)
        predict_class = 'low' if predict_class == 'normalNail' else 'high'

        if format == 'upload':
            build_link('Nail', uid, upload_time, file_name, predict_class)

        # Json response format.
        response = json.jsonify(
            {
                "prediction": predict_class, 
                "prediction_chinese": globals.read_json("./assets/Nail/json/classes.json")[predict_class]
            }
        )

        return response
    
    return server