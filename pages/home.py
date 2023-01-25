import dash_bootstrap_components as dbc
from dash import html

import globals
from components import cover, services

def serve_layout():
    with open(f"{globals.config['text_path']}/subject.txt", 'r') as f:
        subject = f.read()

    with open(f"{globals.config['text_path']}/note.txt", 'r') as f:
        note = f.read()

    layout = html.Div(
        [
            cover.serve(),
            html.H3('【iamSkin 愛美膚】', style={'textAlign': 'center', 'margin-top': '2rem', 'font-weight': 'bold'}),
            html.H5(subject, style={'textAlign': 'center'}),
            html.H6(note, style={'textAlign': 'center', 'color': 'red'}),
            html.Hr(),
            services.serve(),
        ],
    )
    return layout