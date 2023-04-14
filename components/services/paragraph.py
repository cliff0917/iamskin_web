import feffery_antd_components as fac
from dash import html

import globals

def serve(service_type):
    type_chinese = globals.config['chinese'][service_type]['normal']
    predict_text = globals.config['chinese'][service_type]['predict_text']
    type_text = type_chinese + predict_text

    lines = [
        f'AI 評估{type_text}，',
        f'獲取相關照護衛教資訊。'
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