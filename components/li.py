import feffery_antd_components as fac
from dash import html

from components import bold_text

def serve(title, content):
    return html.Li(
        [
            bold_text.serve(title),
            fac.AntdText(content)
        ],
        style={'fontSize': 25}
    )