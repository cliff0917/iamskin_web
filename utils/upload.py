import os
import base64
import requests
from flask import request

def serve(server):
    @server.route('/upload/', methods=['POST'])
    def upload():
        # 獲取上傳 id, 指向 save path
        uploadId = request.values.get('uploadId')

        # 獲取上傳檔案名稱
        filename = request.files['file'].filename

        # 建立上傳 id 的目錄
        try:
            os.mkdir(os.path.join('upload', uploadId))
        except FileExistsError:
            pass

        filepath = os.path.join('upload', uploadId, filename)

        # 將檔案寫到指定目錄
        with open(filepath, 'wb') as f:
            # 每次讀 10 MB
            for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
                f.write(chunk)

        with open(filepath, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())

        response = requests.post(
            'http://0.0.0.0:9487/skin-classifier',
            json={
                'format': 'flask',
                'image': b64_string.decode('ascii'),
            }
        )
        response = response.json()

        return {'filename': filename}

    return server