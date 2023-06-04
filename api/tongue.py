import warnings

warnings.filterwarnings("ignore", category=Warning)

import numpy as np
from flask import request, json
from keras.models import load_model
from PIL import Image

import globals
from utils import mobile, database

def get_post(server):
    service_type = 'Tongue'
    classes = ['black', 'normal', 'white', 'yellow']
    model = load_model(f"./models/{service_type}/classifier.h5")

    @server.route(f"/{service_type}-classifier", methods=["POST"])
    def tongue_classfier():
        # Receive request.
        format = request.form.get('format')
        size = (128, 128)
        upload_time, file_name = '', ''

        if format == 'upload':
            uid, upload_time, file_name, file_path = mobile.save_img(service_type)

        elif format == 'path':
            file_path = request.form.get('path')

        img = Image.open(file_path) 
        img = img.resize(size)
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        predictions = model.predict(img)
        predict_label = np.argmax(predictions[0])
        predict_class = classes[predict_label]
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