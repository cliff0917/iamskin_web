import os
import dash
import json
import requests
import feffery_antd_components as fac
from flask import session
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, MATCH
from datetime import datetime

import globals
from lib import plot, database
from components.modal import share
from components.services import card, result
from components import bold_text, uploader, li, explain_li

def serve_layout(types, tutorial_isOpen):
    with open(f"./assets/{types}/text/card.txt", 'r') as f:
        lines = f.readlines()

    layout = html.Div(
        [
            share.serve(types),
            card.serve(lines[0], lines[1], types),
            uploader.serve(types),
            result.serve(types),
        ],
    )
    return layout


@callback(
    [
        Output({'type': 'upload-text', 'index': MATCH}, 'children'),
        Output({'type': 'upload-img', 'index': MATCH}, 'src'),
        Output({'type': 'output-info', 'index': MATCH}, 'children'),
        Output({'type': 'predict-class', 'index': MATCH}, 'children'),
        Output({'type': 'advice', 'index': MATCH}, 'children'),
        Output({'type': 'share-btn-collapse', 'index': MATCH}, 'is_open'),
    ],
    Input({'type': 'upload', 'index': MATCH}, 'isCompleted'),
    [
        State({'type': 'upload', 'index': MATCH}, 'fileNames'),
        State({'type': 'upload', 'index': MATCH}, 'upload_id'),
    ],
    prevent_initial_call=True
)
def show_upload_status(isCompleted, fileNames, upload_id):
    if isCompleted:
        session["upload_time"] = upload_id.split('/')[-1]
        types = session["cur_path"][1:]
        session["type"] = types
        relative_path = os.path.join('assets/upload', upload_id, fileNames[0])

        # 避免上傳的檔名中含有空白導致 Acne 的 output img 無法顯示
        if ' ' in fileNames[0]:
            fileNames[0] = fileNames[0].replace(' ', '-')
            new_path = relative_path.replace(' ', '-')
            os.system(f'mv "{relative_path}" {new_path}')
            relative_path = new_path

        session["input_path"] = relative_path
        absolute_path = os.path.join(os.getcwd(), relative_path)

        additional_title = dash.no_update
        additional_content = dash.no_update

        url = f"https://{globals.config['domain_name']}/{types}-classifier"
        payload = {'format': 'path', 'path': absolute_path}
        headers = {'Accept': 'application/json'}

        r = requests.post(url, data=payload, headers=headers)
        response = json.loads(r.text)
        # print(response)

        # 建立儲存預測結果的資料夾
        save_path = f'assets/prediction/{upload_id}'
        os.makedirs(save_path, exist_ok=True)

        output_path = os.path.join(save_path, fileNames[0])
        session["output_path"] = output_path

        predict_class = response['prediction']
        predict_class_chinese = globals.read_json(f"./assets/{types}/json/classes.json")[predict_class]
        output_text = html.H3(
            f"預測您的{globals.config['chinese'][types]['normal']}{globals.config['chinese'][types]['predict_text']}為「{predict_class_chinese}」",
            style={'font-weight': 'bold'},
        )

        if types == 'Skin':
            class_name, class_prob = [], []

            for k, v in response['likelihood'].items():
                class_name.append(k)
                class_prob.append(v)

            fig = plot.pie(class_name, class_prob)
            fig.write_image(output_path)
            output_img = fac.AntdImage(
                src=output_path,
                locale='en-us'
            )

            additional_title = f'【{predict_class_chinese}】'

            with open(f'assets/{types}/text/{predict_class}.txt', 'r') as f:
                lines = f.readlines()
                feature = li.serve('特徵：', lines[0])
                maintain = li.serve('護膚重點：', lines[1])
                additional_content = [feature, html.Br(), maintain]

            info = (
                session["google_id"], session["type"], session["upload_time"],
                fileNames[0], -1, '', -1, ''
            )
            database.add_history(info)

            return [
                '上傳的圖片：', relative_path, [output_text, output_img],
                additional_title, additional_content, True
            ]

        elif types == 'Acne':
            additional_title = [
                '【AI 針對預測結果所做出的解釋】',
                fac.AntdTag(
                    content='β測試',
                    color='blue',
                    style={
                        'fontSize': 20,
                        'padding': '7px 7px',
                    },
                )
            ]

            attr_prob = response['attr_prob']

            with open(f'./assets/{types}/text/attributes.txt', 'r') as f:
                attributes = f.read().splitlines()

            additional_content = [
                explain_li.serve(attributes, attr_prob, 21, 23),
                explain_li.serve(attributes, attr_prob, 15, 20),
                explain_li.serve(attributes, attr_prob, 0, 5),
                explain_li.serve(attributes, attr_prob, 5, 7),
                explain_li.serve(attributes, attr_prob, 7, 9),
                explain_li.serve(attributes, attr_prob, 9, 13),
                explain_li.serve(attributes, attr_prob, 13, 15),
            ]

        # 建立 soft link
        os.system(f'ln -s {os.getcwd()}/assets/{types}/img/{predict_class}.png {output_path}')

        output_img = fac.AntdImage(src=output_path, locale='en-us')

        info = (
            session["google_id"], session["type"], session["upload_time"],
            fileNames[0], -1, '', -1, ''
        )
        database.add_history(info)

        return [
            '上傳的圖片：', relative_path, [output_text, output_img],
            additional_title, additional_content, True
        ]
    
    return [None, None, None, None, None, False] # 網頁初始化時沒圖片的狀態

@callback(
    Output({'type': 'share-modal', 'index': MATCH}, 'visible'),
    Input({'type': 'share-btn', 'index': MATCH}, 'nClicks'),
    prevent_initial_call=True
)
def display_output(n_clicks):
    if n_clicks:
        return True
    return dash.no_update