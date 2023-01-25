import dash_bootstrap_components as dbc
from dash import callback
from flask import session
from dash.dependencies import Input, Output, State

def serve():
    if session.get('google_id', None) != None:
        return dbc.Collapse(
            dbc.NavItem(
                dbc.NavLink("登出", id='logout', external_link=True, href="/", n_clicks=0, style={"color": "black"}),
                style={'textAlign': 'center'}
            ),
            is_open=True,
            id='logout-collapse'
        )
    return None


@callback(
    Output("logout-collapse", "is_open"),
    Input("logout", "n_clicks"),
    State("logout-collapse", "is_open"),
    prevent_initial_call=True
)
def clear(n, is_open):
    if n:
        session.clear()
        return not is_open
    return is_open