import os
from flask import request

import globals
from lib import database

# 儲存 app 上傳的圖片
def save_img(service_type):
    uid = request.form.get('uid')
    upload_time = globals.now()
    file = request.files['image']
    file_name = file.filename
    dir_path = build_dir(service_type, uid, upload_time)
    file_path = f'{dir_path}/{file_name}'
    file.save(file_path)
    return uid, upload_time, file_name, file_path


# 建立 app 上傳圖片的資料夾
def build_dir(service_type, uid, upload_time):
    dir_path = f'./assets/web/upload/{service_type}/{uid}/{upload_time}'
    os.makedirs(dir_path, exist_ok=True)
    return dir_path