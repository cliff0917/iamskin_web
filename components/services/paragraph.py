import feffery_antd_components as fac
from dash import html

import globals

def serve(types):
    with open(f"{globals.config['assets_path']}/{types}/text/home_intro.txt", 'r') as f:
        lines = f.readlines()

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