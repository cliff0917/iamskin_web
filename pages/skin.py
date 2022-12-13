from dash import html

from components import card, tutorial, upload

def serve_layout():
    layout = html.Div(
        [
            card.serve(
                '膚質檢測工具',
                '透過影像分析來檢測您的膚質為乾性肌、油肌、敏感肌。',
                True,
                'skin',
            ),
            upload.serve(),
        ],
    )
    return layout