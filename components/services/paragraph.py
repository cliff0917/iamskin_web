import feffery_antd_components as fac
from dash import html

import globals

def serve(service_type):
    type_chinese = globals.config['chinese'][service_type]['normal']
    predict_text = globals.config['chinese'][service_type]['predict_text']
    type_text = type_chinese + predict_text

    lines = [
        f'運用 AI 評估{type_text}，',
        f'取得{type_text}結果圖，',
        f'以及{type_chinese}照護衛教資訊。'
    ]

    paragraph = html.Div(
        [
            html.H4(
                line,
                style={
                    'fontSize': 25,
                    'font-weight': 'bold',
                }
            )
            for line in lines
        ]
    )
    return paragraph