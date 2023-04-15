import os, requests, json
from linebot.models import *

# save line image
def save_img(message_content, dir_path, file_name):
    os.makedirs(dir_path, exist_ok=True) # 建立儲存 input image 的資料夾

    file_path = f'{dir_path}/{file_name}'

    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    return file_path


# 調用 API
def get_result(domain_name, service_type, path):
    url = f"https://{domain_name}/{service_type}-classifier"
    payload = {'format': 'path', 'path': path}
    headers = {'Accept': 'application/json'}
    r = requests.post(url, data=payload, headers=headers)
    response = r.json()
    return response['output_url']


# 取得 target 是否在 service_types 中的 key
def get_key(target, service_types):
    for key, values in service_types.items():
        if target == values['cn']:
            return key, values['en']
    return -1, '' # 若不存在, 則返回 -1


def get_content(config, service_type):
    text = f"歡迎使用{config['chinese'][service_type]['normal']}檢測功能\n\n \
麻煩您拍照或上傳想要分析的照片。\n\n \
照片要確實含有您的{config['chinese'][service_type]['tutorial']}且盡量再充足光源下拍攝，並注意不要「失焦」，否則判讀結果不具任何意義。"
    return text

