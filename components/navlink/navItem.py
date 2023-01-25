from dash import callback
from dash.dependencies import Input, Output, MATCH
import dash_bootstrap_components as dbc

def serve(text, link):
    return dbc.NavItem(
        dbc.NavLink(
            text, external_link=True, href=link, n_clicks=0,
            id={
                'type': 'nav-link',
                'index': text
            },
            style={"color": "black"},
        ), 
        style={'textAlign': 'center'}
    )