import dash_bootstrap_components as dbc
from dash import html

import globals
from components import cover, subject, services

def serve_layout():
    layout = html.Div(
        [
            cover.serve(),
            subject.serve(),
            services.serve(),
        ]
    )
    return layout