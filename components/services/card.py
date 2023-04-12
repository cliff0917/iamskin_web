import feffery_antd_components as fac
from dash import html

from components.services import tutorial

def serve(title, content, service_type):
    card = fac.AntdCard(
        fac.AntdParagraph(
            [
                fac.AntdText(content),
                html.Br(),
                tutorial.serve(service_type),
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
            "background-color": 'white',
        },
    )
    return card