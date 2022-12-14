from dash import callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import globals
from components import logo, login_btn, login_modal

def serve(session):
    navbar = dbc.Navbar(
        [
            logo.serve(),
            dbc.Col(
                style={
                    'width': 4,
                }
            ),
            login_btn.serve(),
            login_modal.serve(),
        ],
        color="#8EA0A5",
        sticky='top',
        style={
            'width':'100%',
            'height':'80px',
        },
    )
    return navbar

@callback(
    Output('modal', 'visible'),
    Input('login-btn', 'nClicks'),
    prevent_initial_call=True
)
def modal_demo_callback1(nClicks):
    return True