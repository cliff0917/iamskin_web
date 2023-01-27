from dash import callback
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc

from components.common_style import navlink_active, navlink_not_active

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
    return [navlink_active if link["index"] == pathname else navlink_not_active for link in links]