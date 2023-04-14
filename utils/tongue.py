import warnings

warnings.filterwarnings("ignore", category=Warning)

from flask import request, json

import globals
from mobile.process import save_img, build_link
from utils.tongue_preprocess import segmentation, classifier

def get_post(server):
    classes = ['black', 'normal', 'white', 'yellow']
    seg_model = segmentation.load_model('./models/tongue/segmentation')
    cls_model = classifier.load_model('./models/tongue/classifier/cnn.pth')

    @server.route("/Tongue-classifier", methods=["POST"])
    def tongue_classfier():
        # Receive request.
        format = request.form.get('format')
        upload_time = ''

        if format == 'upload':
            uid, upload_time, file_name, file_path = save_img('Tongue')

        elif format == 'path':
            file_path = request.form.get('path')

        seg_img = segmentation.predict(seg_model, file_path) # 獲得舌頭切割後的圖片
        predict_class = classifier.predict(cls_model, classes, seg_img)

        if format == 'upload':
            build_link('Tongue', uid, upload_time, file_name, predict_class)

        # Json response format.
        response = json.jsonify(
            {
                "prediction": predict_class,
                "prediction_chinese": globals.read_json("./assets/Tongue/json/classes.json")[predict_class],
                "upload_time": upload_time
            }
        )
        return response

    return server