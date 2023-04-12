import PIL.Image
import numpy as np
import os, cv2
from flask import request, json
from tensorflow.keras.models import load_model

import globals
from mobile.process import save_img, plot_img

def get_post(server):
    model = load_model('./models/Skin.h5')

    @server.route("/Skin-classifier", methods=["POST"])
    def skin_classfier():
        # Receive request.
        format = request.form.get('format')
        size = (224, 224)
        upload_time = ''

        # 從手機上傳
        if format == 'upload':
            uid, upload_time, file_name, file_path = save_img('Skin')

        elif format == 'path':
            file_path = request.form.get('path')

        image = cv2.imread(file_path)
        image = cv2.resize(image, size)
        image = np.expand_dims(np.array(image), axis=0) # / 255

        # Prediction summary.
        classification = {"dry": 0.0, "oily": 0.0, "sensitive": 0.0}
        score = [s for s in model.predict(image).squeeze(0).round(3)]
        likelihood = {k: float(v) for k, v in zip(classification, score)}
        predict_class = max(likelihood, key=likelihood.get)

        with open(f'assets/Skin/text/{predict_class}.txt', 'r') as f:
            lines = f.readlines()
            feature = lines[0]
            maintain = lines[1]

        if format == 'upload':
            plot_img('Skin', uid, upload_time, file_name, likelihood)

        # Json response format.
        response = json.jsonify(
            {
                "likelihood": likelihood, 
                "prediction": predict_class,
                "prediction_chinese": globals.read_json("./assets/Skin/json/classes.json")[predict_class],
                "feature": feature,
                "maintain": maintain,
                "upload_time": upload_time
            }
        )
        return response
        
    return server