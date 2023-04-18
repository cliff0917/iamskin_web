import os, requests, json
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler

import globals

load_dotenv()
globals.initialize()

client_secrets_file = config["google_drive"]["client_secret"]["file_path"]
secret_config = globals.read_json(client_secrets_file)
channel_access_token = secret_config["linebot"]['LINE_CHANNEL_ACCESS_TOKEN']

# 設定圖片與按鈕位置，產生圖文選單 id
headers = {'Authorization': f'Bearer {channel_access_token}', 'Content-Type': 'application/json'}
body = {
    'size': {'width': 2500, 'height': 810},    # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'menu_4',                          # 選單名稱
    'chatBarText': 'AI檢測',                    # 選單在 LINE 顯示的標題
    'areas': [                                  # 選單內容
        {
          'bounds': {'x': 0, 'y': 0, 'width': 625, 'height': 810}, # 選單位置與大小
          'action': {'type': 'message', 'text': '我要檢測 膚質'} # 點擊後傳送文字
        },
        {
          'bounds': {'x': 625, 'y': 0, 'width':625, 'height': 810}, # 選單位置與大小
          'action': {'type': 'message', 'text':'我要檢測 指甲'} # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1250, 'y': 0, 'width':625, 'height': 810}, # 選單位置與大小
          'action': {'type': 'message', 'text':'我要檢測 痘痘'} # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1875, 'y': 0, 'width':625, 'height': 810}, # 選單位置與大小
          'action': {'type': 'message', 'text':'我要檢測 舌頭'} # 點擊後傳送文字
        }
    ]
}

# 向指定網址發送 request
req = requests.request(
    'POST', 'https://api.line.me/v2/bot/richmenu',
    headers=headers,
    data=json.dumps(body).encode('utf-8')
)
rich_menu = req.json()["richMenuId"]
print(rich_menu)

# 將圖文選單綁定圖片
line_bot_api = LineBotApi(channel_access_token)

with open("./richmenu.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu, "image/png", f)

# 將圖文選單與 LINE BOT 綁定
req = requests.request(
    'POST', 
    f'https://api.line.me/v2/bot/user/all/richmenu/{rich_menu}', 
    headers=headers
)

print(req.text)