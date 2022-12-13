from dash import html

from components import card, upload

def serve_layout():
    layout = html.Div(
        [
            card.serve(
                '痘痘檢測工具',
                '透過影像分析來檢測您痘痘的嚴重程度。',
                True,
                'acne',
            ),
            upload.serve(),
        ],
    )
    return layout