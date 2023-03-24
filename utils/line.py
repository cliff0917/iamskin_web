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
    path = './utils'
    create_folder(path)

    channel_secret = config["LINE_CHANNEL_SECRET"]
    channel_access_token = config["LINE_CHANNEL_ACCESS_TOKEN"]
    imgur_client_id = config["IMGUR_CLIENT_ID"]

    if channel_secret is None:
        print("Specify LINE_CHANNEL_SECRET as environment variable.")
        sys.exit(1)
    if channel_access_token is None:
        print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
        sys.exit(1)
    if imgur_client_id is None:
        print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
        sys.exit(1)

    # linebot api setting
    line_bot_api = LineBotApi(channel_access_token)
    handler = WebhookHandler(channel_secret)
    liff_api = LIFF(channel_access_token)

    # save user state
    user_state = {}

    # todo 歡迎頁面選單
    @handler.add(FollowEvent)
    def handel_follow(event):
        profile = line_bot_api.get_profile(event.source.user_id)
        # user_name = profile.display_name #使用者名稱
        uid = profile.user_id # 發訊者ID
        FlexMessage = json.load(open(f'{path}/flexMessage/greet_newFriend.json','r',encoding='utf-8'))

        line_bot_api.push_message(uid, FlexSendMessage('歡迎訊息', FlexMessage))


    # 處理文字訊息
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        msg = str(event.message.text).upper().strip() # 使用者輸入的內容
        profile = line_bot_api.get_profile(event.source.user_id)
        user_name = profile.display_name #使用者名稱
        uid = profile.user_id # 發訊者ID
        # global user_state
        if re.match("AI檢測", msg):
            FlexMessage = json.load(open(f'{path}/flexMessage/AI_detect_menu.json','r',encoding='utf-8'))
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('AI檢測選單', FlexMessage))
        elif re.match("我要檢測 膚質", msg):
            user_state[uid] = 1
            content_text = """歡迎使用膚質檢測功能\n
    我需要影像進行分析，麻煩您拍照或上傳想要分析的照片。\n
    照片要確實含有您的肌膚且盡量再充足光源下拍攝，並注意不要「失焦」，否則判讀結果不具任何意義。"""
            text_message = TextSendMessage(text = content_text)
            line_bot_api.reply_message(event.reply_token, text_message)
            skin_gif_url = "https://i.imgur.com/r4xpSne.gif"
            gif_message = ImageSendMessage(original_content_url = skin_gif_url, preview_image_url = skin_gif_url,
                                        quick_reply=QuickReply(
                                            items=[
                                                QuickReplyButton(
                                                    action=CameraAction(label="拍照")
                                                ),
                                                QuickReplyButton(
                                                    action=CameraRollAction(label="上傳")
                                                ),
                                                QuickReplyButton(
                                                    action=MessageAction(label="如何使用？", text="如何使用"))
                                            ]
                                        ))
            line_bot_api.push_message(uid, gif_message)
        elif re.match("我要檢測 指甲", msg):
            user_state[uid] = 2
            content_text = """歡迎使用指甲檢測功能\n
    我需要影像進行分析，麻煩您拍照或上傳想要分析的照片。\n
    照片要確實含有您的指甲且盡量再充足光源下拍攝，並注意不要「失焦」，否則判讀結果不具任何意義。"""
            text_message = TextSendMessage(text = content_text)
            line_bot_api.reply_message(event.reply_token, text_message)
            nail_gif_url = "https://i.imgur.com/y35SxLg.gif"
            gif_message = ImageSendMessage(original_content_url = nail_gif_url, preview_image_url = nail_gif_url,
                                        quick_reply=QuickReply(
                                            items=[
                                                QuickReplyButton(
                                                    action=CameraAction(label="拍照")
                                                ),
                                                QuickReplyButton(
                                                    action=CameraRollAction(label="上傳")
                                                ),
                                                QuickReplyButton(
                                                    action=MessageAction(label="如何使用？", text="如何使用"))
                                            ]
                                        ))
            line_bot_api.push_message(uid, gif_message)
        elif re.match("我要檢測 痘痘", msg):
            user_state[uid] = 3
            content_text = """歡迎使用痘痘檢測功能\n
    我需要影像進行分析，麻煩您拍照或上傳想要分析的照片。\n
    照片要確實含有您的臉部且盡量再充足光源下拍攝，並注意不要「失焦」，否則判讀結果不具任何意義。"""
            text_message = TextSendMessage(text = content_text)
            line_bot_api.reply_message(event.reply_token, text_message)
            acne_gif_url = "https://i.imgur.com/4fX6F3N.gif"
            gif_message = ImageSendMessage(original_content_url = acne_gif_url, preview_image_url = acne_gif_url,
                                        quick_reply=QuickReply(
                                            items=[
                                                QuickReplyButton(
                                                    action=CameraAction(label="拍照")
                                                ),
                                                QuickReplyButton(
                                                    action=CameraRollAction(label="上傳")
                                                ),
                                                QuickReplyButton(
                                                    action=MessageAction(label="如何使用？", text="如何使用"))
                                            ]
                                        ))
            line_bot_api.push_message(uid, gif_message)
        elif re.match("如何使用", msg):
            manual_url = "https://i.imgur.com/peChM44.png"
            img_message = ImageSendMessage(original_content_url = manual_url, preview_image_url = manual_url,
                            quick_reply=QuickReply(
                                            items=[
                                                QuickReplyButton(
                                                    action=MessageAction(label="進行AI檢測", text="AI檢測")
                                                )
                                            ]
                                        ))
            line_bot_api.reply_message(event.reply_token, img_message)
        elif re.match("膚質資料", msg):
            skin_post_url = "https://linevoom.line.me/post/_dawMj6RwiZsC13Ntyg10eYiFwLfLVISc_jqctqA/1165210923527359525"
            text_message = TextSendMessage(text=skin_post_url,
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="進行AI檢測", text="AI檢測"))
                                ]))
            line_bot_api.reply_message(event.reply_token, text_message)
        elif re.match("指甲資料", msg):
            nail_post_url = "https://linevoom.line.me/post/_dawMj6RwiZsC13Ntyg10eYiFwLfLVISc_jqctqA/1165211007627399630"
            text_message = TextSendMessage(text=nail_post_url,
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="進行AI檢測", text="AI檢測"))
                                ]))
            line_bot_api.reply_message(event.reply_token, text_message)
        elif re.match("痘痘資料", msg):
            acne_post_url = "https://linevoom.line.me/post/_dawMj6RwiZsC13Ntyg10eYiFwLfLVISc_jqctqA/1165211029027409298"
            text_message = TextSendMessage(text=acne_post_url,
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="進行AI檢測", text="AI檢測"))
                                ]))
            line_bot_api.reply_message(event.reply_token, text_message)
        else:   # 錯誤指令，提供快速回覆
            text_message = TextSendMessage(
                                        text = "請入正確指令" ,
                                        quick_reply=QuickReply(
                                            items=[
                                                QuickReplyButton(
                                                    action=MessageAction(label="進行AI檢測", text="AI檢測")
                                                ),
                                                QuickReplyButton(
                                                    action=MessageAction(label="我要檢測 膚質", text="我要檢測 膚質")
                                                ),
                                                QuickReplyButton(
                                                    action=MessageAction(label="我要檢測 指甲", text="我要檢測 指甲")
                                                ),
                                                QuickReplyButton(
                                                    action=MessageAction(label="我要檢測 痘痘", text="我要檢測 痘痘")
                                                ),
                                                QuickReplyButton(
                                                    action=MessageAction(label="如何使用", text="如何使用")
                                                )
                                            ]
                                        ))
            line_bot_api.reply_message(event.reply_token, text_message)


    # 處理圖片訊息
    @handler.add(MessageEvent, message=ImageMessage)
    def handle_img(event):
        profile = line_bot_api.get_profile(event.source.user_id)
        # user_name = profile.display_name #使用者名稱
        uid = profile.user_id # 發訊者ID
        message_id = event.message.id
        reply_token = event.reply_token

        if user_state.get(uid) == 1: # 膚質
            message_content = line_bot_api.get_message_content(message_id)
            file_path = f"{path}/Image/skin/{reply_token}.jpg"
            save_img(message_content, file_path) # 儲存使用者傳的照片
            img_url = upload_img_to_imgur(imgur_client_id, file_path) # 將存下來的照片上傳至imgur
            res = get_skin_result(img_url)
            result_path = f"{path}/Prediction/skin/{reply_token}_prediction.jpg"
            skin_plot(res['likelihood'], result_path)
            result_url = upload_img_to_imgur(imgur_client_id, result_path)
            img_message = ImageSendMessage(original_content_url = result_url, preview_image_url = result_url,
                                            quick_reply=QuickReply(
                                                items=[
                                                    QuickReplyButton(
                                                        action=MessageAction(label="查看相關資料", text="膚質資料")
                                                    ),
                                                    QuickReplyButton(
                                                        action=MessageAction(label="進行AI檢測", text="AI檢測")
                                                    )
                                                ]
                                            ))
            line_bot_api.reply_message(event.reply_token, img_message)
            # os.remove(file_path) # 將照片刪除
            # os.remove(result_path)
            user_state[uid] = 0

        elif user_state.get(uid) == 2: # 指甲
            message_content = line_bot_api.get_message_content(message_id)
            file_path = f"{path}/Image/nail/{reply_token}.jpg"
            save_img(message_content, file_path)

            img_url = upload_img_to_imgur(imgur_client_id, file_path)
            res = get_nail_result(img_url)

            if res['prediction'] == 'low':
                FlexMessage = json.load(open(f'{path}/flexMessage/nail_result_low.json','r',encoding='utf-8'))
                line_bot_api.reply_message(event.reply_token, FlexSendMessage('指甲異常風險-低', FlexMessage))
            else:
                FlexMessage = json.load(open(f'{path}/flexMessage/nail_result_high.json','r',encoding='utf-8'))
                line_bot_api.reply_message(event.reply_token, FlexSendMessage('指甲異常風險-高', FlexMessage))

            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(res)))
            # os.remove(file_path)
            user_state[uid] = 0

        elif user_state.get(uid) == 3: # 痘痘
            message_content = line_bot_api.get_message_content(message_id)
            file_path = f"{path}/Image/acne/{reply_token}.jpg"
            save_img(message_content, file_path)
            res = get_acne_result(file_path)

            if res['prediction'] == 'low': # low
                FlexMessage = json.load(open(f'{path}/flexMessage/acne_result_low.json','r',encoding='utf-8'))
                line_bot_api.reply_message(event.reply_token, FlexSendMessage('痘痘異常風險-低', FlexMessage))
            else: # high
                FlexMessage = json.load(open(f'{path}/flexMessage/acne_result_high.json','r',encoding='utf-8'))
                line_bot_api.reply_message(event.reply_token, FlexSendMessage('痘痘異常風險-高', FlexMessage))
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已完成痘痘檢測"))
            user_state[uid] = 0
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇檢測項目再上傳圖片"))

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