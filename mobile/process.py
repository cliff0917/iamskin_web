import os
from flask import request

import globals
from lib import plot, database

def save_img(types):
    uid = request.form.get('uid')
    upload_time = globals.now()
    file = request.files['image']
    file_name = file.filename
    dir_path = build_dir('upload', types, uid, upload_time)
    file_path = f'{dir_path}/{file_name}'
    file.save(file_path)
    return uid, upload_time, file_name, file_path


# 建立 img dir
def build_dir(mode, types, uid, upload_time):
    dir_path = f'./assets/web/{mode}/{types}/{uid}/{upload_time}'
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


# 目前只有 Skin 需要畫圖, 其他的都是建立 soft link 到指定的 img
def plot_img(types, uid, upload_time, file_name, likelihood):
    dir_path = build_dir('predict', types, uid, upload_time)
    output_path = f'{dir_path}/{file_name}'
    plot.pie(likelihood, output_path) # 畫圖並將其存在 output_path
    add_record(types, uid, upload_time, file_name) # 將 app 的資訊加入到 DB 中


def build_link(types, uid, upload_time, file_name, predict_class):
    dir_path = build_dir('predict', types, uid, upload_time)
    output_path = f'{dir_path}/{file_name}'
    os.system(f'ln -s {os.getcwd()}/assets/{types}/img/{predict_class}.png {output_path}')
    add_record(types, uid, upload_time, file_name) # 將 app 的資訊加入到 DB 中


def add_record(types, uid, upload_time, file_name):
    info = (uid, types, upload_time, file_name, -1, '', -1, '')
    database.add_history(info)