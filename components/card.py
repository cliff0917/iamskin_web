import feffery_antd_components as fac
from dash import html

from components import tutorial

def serve(title, content, margin_top=None, tutorial_is_open=False, types='Skin'):
    card = fac.AntdCard(
        fac.AntdParagraph(
            [
                fac.AntdText(content),
                html.Br(),
                tutorial.serve(tutorial_is_open, types), # 是否顯示使用教學
            ]
        ),
        title=title,
        headStyle={
            'fontSize': 35,
            'font-weight': 'bold',
        },
        hoverable=True,
        bodyStyle={
            'fontSize': 30,
        },
        style={
            "margin-top": margin_top,
        },
    )
    return card