import PIL.Image
import numpy as np
import os, cv2
from flask import request, json
from tensorflow.keras.models import load_model

def get_post(server):
    model = load_model('./models/Nail.h5')

    @server.route("/Nail-classifier", methods=["POST"])
    def nail_classifier():
        # Receive request.
        format = request.form.get('format')
        size = (224, 224)

        if format == 'upload':
            file = request.files['image']
            file_path = os.path.join('./assets/app/upload/Nail', file.filename)
            file.save(file_path)

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
        prediction = 'low' if predict_class == 'normalNail' else 'high'

        # Json response format.
        response = json.jsonify(
            {"prediction": prediction}
        )

        return response
    
    return server