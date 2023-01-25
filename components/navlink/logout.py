import dash_bootstrap_components as dbc
from dash import html, callback
from flask import session
from dash.dependencies import Input, Output, State

from components.img import avatar

def serve():
    if session.get('picture', None) != None:
        return dbc.NavItem(
            html.A(
                dbc.Row(
                    [
                        avatar.serve(),
                        dbc.Collapse(
                            dbc.NavLink("登出", external_link=True, href="/", n_clicks=0, style={"color": "black"}),
                            is_open=True,
                            id='logout-collapse'
                        )
                    ],
                ),
                id='logout',
                n_clicks=0,
                href='/',
            ),
            className='mx-auto'
        )
    return None
    

# 點擊登出後, 清除 cookie 且隱藏登出鍵
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