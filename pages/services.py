import os
import dash
import json
import requests
import feffery_antd_components as fac
from flask import session
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, MATCH
from datetime import datetime

import globals, database, plot
from components.modal import share
from components.services import card, result
from components import uploader

def serve_layout(types, tutorial_isOpen):
    with open(f"{globals.config['assets_path']}/{types}/text/card.txt", 'r') as f:
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
        Output({'type': 'horizon-line', 'index': MATCH}, 'is_open'),
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
        session["predict_time"] = globals.now()
        types = session["cur_path"][1:]
        session["type"] = types
        relative_path = os.path.join('assets/upload', upload_id, fileNames[0])
        absolute_path = os.path.join(os.getcwd(), relative_path)
        session["input_path"] = relative_path

        ip_address = requests.get('https://api.ipify.org').text
        r = requests.post(
            f"http://{ip_address}:{globals.config['port'][types]}/{types}-classifier",
            json={
                'format': 'path',
                'image': absolute_path
            }
        )
        response = json.loads(r.text)
        # print(response)

        if types == 'Skin':
            col_name = [col for col in response['likelihood'].keys()]
            col_val = [float(value) for value in response['likelihood'].values()]

            predict_class = [c for c in response['prediction'].keys()][0]
            predict_class_chinese = globals.read_json(f'{globals.config["assets_path"]}/{types}/json/classes.json')[predict_class]

            output_text = html.H3(
                f'預測您的膚質為「{predict_class_chinese}」',
                style={
                    'font-weight': 'bold'
                },
            )

            # 建立儲存預測結果的資料夾
            save_path = 'assets/prediction'
            for dir_name in upload_id.split('/'):
                save_path = os.path.join(save_path, dir_name)
                globals.mkdir(save_path)

            filepath = os.path.join(save_path, fileNames[0])
            session['output_path'] = filepath

            fig = plot.pie(col_name, col_val)
            fig.write_image(filepath)
            output_img = fac.AntdImage(
                src=filepath,
                locale='en-us'
            )

            with open(f'assets/{types}/text/{predict_class}.txt', 'r') as f:
                lines = f.readlines()
                feature = html.Li(
                    [
                        fac.AntdText('特徵：', style={'font-weight': 'bold'}),
                        fac.AntdText(lines[0])
                    ],
                    style={'fontSize': 25}
                )
                maintain = html.Li(
                    [
                        fac.AntdText('護膚重點：', style={'font-weight': 'bold'}),
                        fac.AntdText(lines[1])
                    ],
                    style={'fontSize': 25}
                )

            info = (
                session["google_id"], session["type"], session["predict_time"],
                session["input_path"], session['output_path'], -1, '', -1, ''
            )
            database.add_history(info)

            return [
                '上傳的圖片：', relative_path, [output_text, output_img],
                False, f'【{predict_class_chinese}】', [feature, html.Br(), maintain], True
            ]
        
        elif types == 'Nail':
            if list(response['prediction'].keys())[0] == 'normalnail':
                session['output_path'] = f'assets/{types}/img/low.png'
                predict_class_chinese = '低'
            else:
                session['output_path'] = f'assets/{types}/img/high.png'
                predict_class_chinese = '高'

            output_text = html.H3(
                f'預測您的指甲異常風險為「{predict_class_chinese}」',
                style={'font-weight': 'bold'},
            )
            

        elif types == 'Acne':
            predict_class = response['prediction']
            predict_class_chinese = globals.read_json(f'{globals.config["assets_path"]}/{types}/json/classes.json')[predict_class]
            output_text = html.H3(
                f'預測您的痘痘嚴重程度為「{predict_class_chinese}」',
                style={'font-weight': 'bold'},
            )
            session['output_path'] = f'assets/{types}/img/{predict_class}.png'
        
        output_img = fac.AntdImage(src=session['output_path'], locale='en-us')

        info = (
            session["google_id"], session["type"], session["predict_time"],
            session["input_path"], session['output_path'], -1, '', -1, ''
        )
        database.add_history(info)

    return [
        '上傳的圖片：', relative_path, [output_text, output_img],
        True, dash.no_update, dash.no_update, True
    ]


@callback(
    Output({'type': 'share-modal', 'index': MATCH}, 'visible'),
    Input({'type': 'share-btn', 'index': MATCH}, 'nClicks'),
    prevent_initial_call=True
)
def display_output(n_clicks):
    if n_clicks:
        return True
    return dash.no_update