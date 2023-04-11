import PIL.Image
import numpy as np
import os, cv2
from flask import request, json
from tensorflow.keras.models import load_model

def get_post(server):
    model = load_model('./models/Skin.h5')

    @server.route("/Skin-classifier", methods=["POST"])
    def skin_classfier():
        # Receive request.
        format = request.form.get('format')
        size = (224, 224)

        if format == 'upload':
            file = request.files['image']
            file_path = os.path.join('./assets/web/upload/Skin', file.filename)
            file.save(file_path)

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

        # Json response format.
        response = json.jsonify(
            {"likelihood": likelihood, "prediction": predict_class}
        )
        return response
        
    return server