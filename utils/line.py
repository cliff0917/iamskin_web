from crypt import methods
import os
import sys
import re
import json
from flask import Flask, jsonify, request, abort, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from linebot_utils import *
from liffpy import (LineFrontendFramework as LIFF, ErrorResponse)

def get_post(server, config):
    domain_name = config['domain_name']
    path_url = f"https://{domain_name}/assets"

    channel_secret = config["LINE_CHANNEL_SECRET"]
    channel_access_token = config["LINE_CHANNEL_ACCESS_TOKEN"]

    if channel_secret is None:
        print("Specify LINE_CHANNEL_SECRET as environment variable.")
        sys.exit(1)
    if channel_access_token is None:
        print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
        sys.exit(1)

    # linebot api setting
    line_bot_api = LineBotApi(channel_access_token)
    handler = WebhookHandler(channel_secret)
    liff_api = LIFF(channel_access_token)

    # save user state
    user_state = {}

    # service 對應中、英文, e.g. {1: {'en': 'Skin', 'cn': '膚質'}, ...}
    service_types = {
        i : {'en': key, 'cn': value['normal']} 
        for i, (key, value) in enumerate(config['chinese'].items(), start=1)
    }

    # 歡迎頁面選單
    @handler.add(FollowEvent)
    def handel_follow(event):
        profile = line_bot_api.get_profile(event.source.user_id)
        uid = profile.user_id # 發訊者ID
        FlexMessage = json.load(open('./assets/flexMessage/greet_newFriend.json', 'r', encoding='utf-8'))
        line_bot_api.push_message(uid, FlexSendMessage('歡迎訊息', FlexMessage))


    # 處理文字訊息
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        msg = str(event.message.text).upper().strip() # 使用者輸入的內容
        profile = line_bot_api.get_profile(event.source.user_id)
        user_name = profile.display_name # 使用者名稱
        uid = profile.user_id # 發訊者ID

        # global user_state
        if re.match("AI檢測", msg):
            FlexMessage = json.load(open('./assets/flexMessage/AI_detect_menu.json', 'r', encoding='utf-8'))
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('AI檢測選單', FlexMessage))

        # msg == 我要檢測 XX
        elif ' ' in msg:
            word_list = msg.split(' ')
            prefix, suffix = word_list[0], word_list[-1]
            key, service_type = get_key(suffix, service_types)

            if len(word_list) == 2 and prefix == '我要檢測' and key != -1:
                user_state[uid] = key
                content_text = get_content(config, service_type)
                text_message = TextSendMessage(
                    text=content_text,
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=CameraAction(label="拍照")),
                            QuickReplyButton(action=CameraRollAction(label="上傳")),
                            QuickReplyButton(action=MessageAction(label="如何使用？", text="如何使用"))
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, text_message)

        elif re.match("如何使用", msg):
            manual_url = "https://i.imgur.com/peChM44.png"
            img_message = ImageSendMessage(
                original_content_url=manual_url,
                preview_image_url=manual_url,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="進行AI檢測", text="AI檢測"))
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, img_message)

        # msg == XX資料
        elif "資料" in msg:
            prefix = msg.replace('資料', '')
            key, service_type = get_key(prefix, service_types)
            post_url = f"https://linevoom.line.me/post/_dawMj6RwiZsC13Ntyg10eYiFwLfLVISc_jqctqA/{config['line_post'][service_type]}"
            text_message = TextSendMessage(
                text=post_url,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="進行AI檢測", text="AI檢測"))
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, text_message)

        else: # 錯誤指令，提供快速回覆
            text_message = TextSendMessage(
                text = "請入正確指令" ,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="進行AI檢測", text="AI檢測")),
                        QuickReplyButton(action=MessageAction(label="我要檢測 膚質", text="我要檢測 膚質")),
                        QuickReplyButton(action=MessageAction(label="我要檢測 指甲", text="我要檢測 指甲")),
                        QuickReplyButton(action=MessageAction(label="我要檢測 痘痘", text="我要檢測 痘痘")),
                        QuickReplyButton(action=MessageAction(label="如何使用", text="如何使用"))
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, text_message)

    # 處理圖片訊息
    @handler.add(MessageEvent, message=ImageMessage)
    def handle_img(event):
        profile = line_bot_api.get_profile(event.source.user_id)
        
        uid = profile.user_id # 發訊者ID
        message_id = event.message.id
        reply_token = event.reply_token

        status = user_state.get(uid)

        message_content = line_bot_api.get_message_content(message_id)
        service_type = service_types[status]['en']
        service_type_chinese = service_types[status]['cn']

        dir_path = f"./assets/linebot/upload/{service_type}"
        file_name = f"{reply_token}.jpg"
        file_path = save_img(message_content, dir_path, file_name) # 儲存使用者傳的照片
        output_url = get_result(domain_name, service_type, file_path)

        img_message = ImageSendMessage(
            original_content_url=output_url, 
            preview_image_url=output_url,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="查看相關資料", text=f"{service_type_chinese}資料")),
                    QuickReplyButton(action=MessageAction(label="進行AI檢測", text="AI檢測"))
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, img_message)
        user_state[uid] = 0

    @server.route("/Linebot", methods=["POST"])
    def linebot():
        # get X-Line-Signature header value
        signature = request.headers["X-Line-Signature"]

        # get request body as text
        body = request.get_data(as_text=True)
        server.logger.info("Request body: " + body)

        # parse webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        return "OK"

    return server