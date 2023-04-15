import warnings

warnings.filterwarnings("ignore", category=Warning)

from flask import request, json

import globals
from mobile.process import save_img
from utils.tongue_preprocess import segmentation, classifier
from lib import database

def get_post(server):
    service_type = 'Tongue'
    classes = ['black', 'normal', 'white', 'yellow']
    seg_model = segmentation.load_model('./models/tongue/segmentation')
    cls_model = classifier.load_model('./models/tongue/classifier/cnn.pth')

    @server.route(f"/{service_type}-classifier", methods=["POST"])
    def tongue_classfier():
        # Receive request.
        format = request.form.get('format')
        upload_time, file_name = '', ''

        if format == 'upload':
            uid, upload_time, file_name, file_path = save_img(service_type)

        elif format == 'path':
            file_path = request.form.get('path')

        seg_img = segmentation.predict(seg_model, file_path) # 獲得舌頭切割後的圖片
        predict_class = classifier.predict(cls_model, classes, seg_img)
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