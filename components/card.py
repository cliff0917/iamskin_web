import feffery_antd_components as fac
from dash import html

from components import tutorial

def serve(title, content, tutorial_is_open=False, types='Skin'):
    card = fac.AntdCard(
        fac.AntdParagraph(
            [
                fac.AntdText(content),
                html.Br(),
                tutorial.serve(tutorial_is_open, types),
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
            "margin-top": "2rem",
        },
    )
    return card