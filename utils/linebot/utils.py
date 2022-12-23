import os
import sys
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, MessageTemplateAction, TemplateSendMessage, ButtonsTemplate
import matplotlib
import matplotlib.pyplot as plt
import pyimgur
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import globals

matplotlib.use('Agg')

globals.initialize()

ip_address = requests.get('https://api.ipify.org').text
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", globals.config["LINE_CHANNEL_ACCESS_TOKEN"])

if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1) 


# create needed folder
def create_folder():
    folder_list = ["./Image", "./Image/skin", "Image/nail", "Image/acne", "./Prediction", "./Prediction/skin"]
    for dir in folder_list:
        if not os.path.exists(dir):
            os.mkdir(dir)


# save line image
def save_img(message_content, file_path):
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

# upload img to imgur, return url
def upload_img_to_imgur(client_id, imgpath):
	im = pyimgur.Imgur(client_id)
	upload_image = im.upload_image(imgpath, title="Uploaded with PyImgur")
	return upload_image.link


# skin type
def get_skin_result(url):
    skin_model_url = f"http://{ip_address}:{globals.config['port']['Skin']}/Skin-classifier"
    r = requests.post(
        skin_model_url,
        data=json.dumps({
            'image': url, 'format': "url"}),
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
def get_nail_result(url):
    nail_model_url = f"http://{ip_address}:{globals.config['port']['Nail']}/Nail-classifier"
    r = requests.post(
        nail_model_url,
        data=json.dumps({
            'image': url, 'format': "url"}),
        timeout=(2, 15),
        headers={'Content-Type': 'application/json', 'Accept': 'text/plain'})

    response = r.json()
    return response


def get_acne_result(url):
    r = requests.post(
        f"http://{ip_address}:{globals.config['port']['Acne']}/Acne-classifier",
        data=json.dumps({
            'image': url, 'format': "url"}),
        timeout=(2, 15),
        headers={'Content-Type': 'application/json', 'Accept': 'text/plain'})

    response = r.json()
    return response