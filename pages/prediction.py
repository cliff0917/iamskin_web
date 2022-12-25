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
    State({'type': 'upload', 'index': MATCH}, 'fileNames'),
    prevent_initial_call=True
)
def show_upload_status(isCompleted, fileNames):
    if isCompleted:
        types = session["cur_path"][1:]
        relative_path = os.path.join('assets/upload', types, fileNames[0])
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

        if types == 'Skin':
            col_name = [col for col in response['likelihood'].keys()]
            col_val = [float(value) for value in response['likelihood'].values()]

            predict_class = [c for c in response['prediction'].keys()][0]
            predict_class_chinese = globals.config["Skin-mapping"][predict_class]

            output_text = html.H3(
                f'預測您的膚質為「{predict_class_chinese}」',
                style={
                    'font-weight': 'bold'
                },
            )

            # 建立儲存預測結果的資料夾
            type_path = os.path.join('assets/prediction', types)
            globals.build_dir(type_path)
            save_path = os.path.join(type_path, globals.now())
            globals.build_dir(save_path)

            filepath = os.path.join(save_path, fileNames[0])
            session['filepath'] = filepath

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
            True, predict_class_chinese, [feature, maintain], True
        ]

    return dash.no_update


@callback(
    Output({'type': 'share-modal', 'index': MATCH}, 'visible'),
    Input({'type': 'share-btn', 'index': MATCH}, 'nClicks'),
    prevent_initial_call=True
)
def display_output(n_clicks):
    if n_clicks:
        return True
    return dash.no_update