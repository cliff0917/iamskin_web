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
from components import card, uploader, result

def serve_layout(types, tutorial_isOpen):
    layout = html.Div(
        [
            # fac.AntdModal(
            #     visible=False,
            #     title=f'{globals.config["service_intro"][types]["title"][:-2]}結果',
            #     renderFooter=False,
            #     id={
            #         'type': 'output-modal',
            #         'index': types
            #     },
            # ),
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
        Output({'type': 'share-btn', 'index': MATCH}, 'is_open'),
    ],
    Input({'type': 'upload', 'index': MATCH}, 'isCompleted'),
    State({'type': 'upload', 'index': MATCH}, 'fileNames'),
    prevent_initial_call=True
)
def show_upload_status(isCompleted, fileNames):
    if isCompleted:
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        types = triggered_id.split(',')[0].split('"')[-2]

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

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 建立儲存預測結果的資料夾
            type_path = os.path.join('assets/prediction', types)
            globals.build_dir(type_path)
            save_path = os.path.join(type_path, now)
            globals.build_dir(save_path)

            fig=plot.pie(col_name, col_val)
            fig.write_image(os.path.join(save_path, fileNames[0]))
            output_img = dcc.Graph(
                figure=fig,
                config= {'displaylogo': False}
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


# @callback(
#     [
#         Output({'type': 'modal', 'index': MATCH}, 'visible'),
#         Output({'type': 'modal', 'index': MATCH}, 'children'),
#     ],
#     Input({'type': 'output', 'index': MATCH}, 'children'),
# )
# def display_output(output):
#     return [True, output]