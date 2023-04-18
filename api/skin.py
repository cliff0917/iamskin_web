import PIL.Image
import numpy as np
import os, cv2
from flask import request, json
from tensorflow.keras.models import load_model

import globals
from utils import mobile, database

def get_post(server):
    service_type = 'Skin'
    model = load_model(f'./models/{service_type}/classifier.h5')

    @server.route(f"/{service_type}-classifier", methods=["POST"])
    def skin_classfier():
        # Receive request.
        format = request.form.get('format')
        size = (224, 224)
        upload_time, file_name = '', ''

        # 從手機上傳
        if format == 'upload':
            uid, upload_time, file_name, file_path = mobile.save_img(service_type)

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
                "upload_time": upload_time,
                "output_url": output_url,
                "file_name": file_name
            }
        )
        return response
        
    return server