import os
from flask import request

import globals
from lib import plot, database

# 儲存 app 上傳的影片
def save_img(service_type):
    uid = request.form.get('uid')
    upload_time = globals.now()
    file = request.files['image']
    file_name = file.filename
    dir_path = build_dir('upload', service_type, uid, upload_time)
    file_path = f'{dir_path}/{file_name}'
    file.save(file_path)
    return uid, upload_time, file_name, file_path


# 建立 img dir
def build_dir(mode, service_type, uid, upload_time):
    dir_path = f'./assets/web/{mode}/{service_type}/{uid}/{upload_time}'
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


# 建立 soft link
def build_link(service_type, uid, upload_time, file_name, predict_class):
    dir_path = build_dir('predict', service_type, uid, upload_time)
    output_path = f'{dir_path}/{file_name}'
    os.system(f'ln -s {os.getcwd()}/assets/{service_type}/img/{predict_class}.png {output_path}')
    add_record(service_type, uid, upload_time, file_name) # 將 app 的資訊加入到 DB 中


def add_record(service_type, uid, upload_time, file_name):
    info = (uid, service_type, upload_time, file_name, -1, '', -1, '')
    database.add_history(info)