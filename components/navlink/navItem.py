from dash import callback
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc

def serve(text, link):
    return dbc.NavItem(
        dbc.NavLink(
            text, external_link=True, href=link,
            id={
                'type': 'nav-link',
                'index': link
            },
            style={"color": "black"},
        ),
        style={'textAlign': 'center'}
    )

@callback(
    Output({'type': 'nav-link', 'index': ALL}, 'style'),
    [
        Input("url", "pathname"),
        Input({'type': 'nav-link', 'index': ALL}, 'id'),
    ],
    prevent_initial_call=True
)
def selected(pathname, links):
    return [{"color": "blue"} if link["index"] == pathname else {"color": "black"} for link in links]