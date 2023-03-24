import os
import sys
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, MessageTemplateAction, TemplateSendMessage, ButtonsTemplate
import matplotlib
import matplotlib.pyplot as plt
import requests
import json

matplotlib.use('Agg')

# create needed folder
def create_folder(path):
    folder_list = [f"{path}/linebot_upload", f"{path}/linebot_upload/Skin", f"{path}/linebot_upload/Nail", f"{path}/linebot_upload/Acne", 
                   f"{path}/linebot_predict", f"{path}/linebot_predict/Skin"]

    for dir in folder_list:
        if not os.path.exists(dir):
            os.mkdir(dir)


# save line image
def save_img(message_content, file_path):
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)


# skin type
def get_skin_result(path):
    r = requests.post(
        "https://iamskin.tk/Skin-classifier",
        data=json.dumps({
            'image': path, 'format': "path"}),
        timeout=(2, 15),
        headers={'Content-Type': 'application/json', 'Accept': 'text/plain'})
    response = r.json()
    return response


def skin_plot(likelihood, path):
    labels = []  # 製作圓餅圖的類別標籤
    size = []  # 製作圓餅圖的數值來源
    for key in likelihood.keys():
        labels.append(key)
        size.append(likelihood.get(key))

    separeted = [0, 0, 0]  # 依據類別數量，分別設定要突出的區塊
    max_val = size.index(max(size))
    separeted[max_val] = 0.1

    colors = ['tomato', 'lightskyblue', 'goldenrod']  # 圓餅圖顏色

    plt.figure(figsize=(9, 6))  # 顯示圖框架大小
    plt.pie(size,  # 數值
            labels=labels,  # 標籤
            autopct="%1.1f%%",  # 將數值百分比並留到小數點一位
            explode=separeted,  # 突出的區塊
            pctdistance=0.6,  # 數字距圓心的距離
            colors=colors,  # 顏色
            textprops={"fontsize": 12},  # 文字大小
            shadow=True)  # 設定陰影
    plt.axis('equal')  # 使圓餅圖比例相等
    plt.title("Pie chart of skin type", {"fontsize": 18})  # 設定標題及其文字大小
    plt.legend(loc="best")  # 設定圖例及其位置為最佳
    plt.savefig(path,  # 儲存圖檔
                bbox_inches='tight',  # 去除座標軸占用的空間
                pad_inches=0.5)  # 去除所有白邊
    plt.close()      # 關閉圖表    


# nail type
def get_nail_result(path):
    r = requests.post(
        "https://iamskin.tk/Nail-classifier",
        data=json.dumps({
            'image': path, 'format': "path"}),
        timeout=(2, 15),
        headers={'Content-Type': 'application/json', 'Accept': 'text/plain'})

    response = r.json()
    return response


def get_acne_result(file_path):
    r = requests.post(
        "https://iamskin.tk/Acne-classifier",
        data=json.dumps(
            {'image': file_path, 'format': 'linebot'}, 
        ),
        timeout=(2, 15),
        headers={'Content-Type': 'application/json', 'Accept': 'text/plain'}
    )

    response = r.json()
    return response