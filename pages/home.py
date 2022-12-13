import dash_bootstrap_components as dbc
from dash import html

import globals
from components import cover, card, services

def serve_layout():
    with open(f"{globals.config['text_path']}/subject.txt", 'r') as f:
        subject = f.read()

    layout = html.Div(
        [
            cover.serve(),
            card.serve('主旨', subject),
            services.serve(),
        ]
    )
    return layout