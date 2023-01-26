from dash import callback
from dash.dependencies import Input, Output, ALL
import dash_bootstrap_components as dbc

def serve(text, link):
    return dbc.NavItem(
        dbc.DropdownMenuItem(
            text, external_link=True, href=link, 
            id={
                'type': 'nav-dropdown-link',
                'index': link
            },
        ),
        style={'textAlign': 'center', 'fontSize': 18}
    )


@callback(
    Output({'type': 'nav-dropdown-link', 'index': ALL}, 'active'),
    [
        Input("url", "pathname"),
        Input({'type': 'nav-dropdown-link', 'index': ALL}, 'id'),
    ],
    prevent_initial_call=True
)
def selected(pathname, links):
    return [True if link["index"] == pathname else False for link in links]