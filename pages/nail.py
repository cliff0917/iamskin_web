from dash import html

from components import card, upload

def serve_layout():
    layout = html.Div(
        [
            card.serve(
                '指甲檢測工具',
                '透過影像分析來檢測您的指甲異常風險。',
                True,
                'nail',
            ),
            upload.serve(),
        ],
    )
    return layout