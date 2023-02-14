import feffery_antd_components as fac
from dash import html

from components import bold_text

def serve(text, attr_prob, lower, upper):
    idx = attr_prob.index(max(attr_prob[lower:upper]))

    return html.Li(
        [
            bold_text.serve(f"{text[idx].split('-')[0]}："),
            fac.AntdText(text[idx].split('-')[-1])
        ],
        style={'fontSize': 25}
    )