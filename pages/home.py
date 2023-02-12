import dash_bootstrap_components as dbc
from dash import html

from components.services import all_services
from components.img import cover

def serve_layout():
    with open("./assets/common/text/subject.txt", 'r') as f:
        subject = f.read()

    with open("./assets/common/text/note.txt", 'r') as f:
        note = f.read()

    layout = html.Div(
        [
            cover.serve(),
            html.H3('【愛美膚 iamSkin】', style={'textAlign': 'center', 'margin-top': '2rem', 'font-weight': 'bold'}),
            html.H5(subject, style={'textAlign': 'center'}),
            html.H6(note, style={'textAlign': 'center', 'color': 'red'}),
            html.Hr(),
            all_services.serve(),
        ],
    )
    return layout