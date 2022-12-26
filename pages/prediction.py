import os
import dash
import json
import requests
import feffery_antd_components as fac
from flask import session
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, MATCH
from datetime import datetime

import globals, plot
from components import card, uploader, result, share_modal

def serve_layout(types, tutorial_isOpen):
    layout = html.Div(
        [
            share_modal.serve(types),
            card.serve(
                globals.config["service_intro"][types]["title"],
                globals.config["service_intro"][types]["content"],
                None,
                tutorial_isOpen,
                types,
            ),
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
        types = session["cur_path"][1:]
        session["type"] = types
        relative_path = os.path.join('assets/upload', upload_id, fileNames[0])
        absolute_path = os.path.join(os.getcwd(), relative_path)
        # print(absolute_path)

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
            predict_class_chinese = globals.config["Classify"][types][predict_class]

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

            fig=plot.pie(col_name, col_val)
            fig.write_image(filepath)
            output_img = dcc.Graph(
                figure=fig,
                config={'displaylogo': False}
            )

            with open(f'assets/text/{predict_class}.txt', 'r') as f:
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

            return [
                '上傳的圖片：', relative_path, [output_text, output_img],
                False, predict_class_chinese, [feature, maintain], True
            ]
        
        elif types == 'Nail':
            if list(response['prediction'].keys())[0] == 'normalnail':
                session['output_path'] = f'assets/img/{types}/low.png'
                predict_class_chinese = '低'
            else:
                session['output_path'] = f'assets/img/{types}/high.png'
                predict_class_chinese = '高'

            output_text = html.H3(
                f'預測您的指甲之異常風險為「{predict_class_chinese}」',
                style={
                    'font-weight': 'bold'
                },
            )
            output_img = fac.AntdImage(
                src=session['output_path'],
                preview=False,
            )

        elif types == 'Acne':
            predict_class = response['prediction']
            predict_class_chinese = globals.config["Classify"][types][predict_class]

            output_text = html.H3(
                f'預測您的痘痘嚴重程度為「{predict_class_chinese}」',
                style={
                    'font-weight': 'bold'
                },
            )

            session['output_path'] = f'assets/img/{types}/{predict_class}.png'
            output_img = fac.AntdImage(
                src=session['output_path'],
                preview=False,
            )

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