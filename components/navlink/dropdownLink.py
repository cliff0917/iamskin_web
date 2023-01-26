import dash_bootstrap_components as dbc

def serve(text, link):
    return dbc.NavItem(
        dbc.DropdownMenuItem(
            text, external_link=True, href=link, 
            id={
                'type': 'nav-link',
                'index': link
            },
        ),
        style={'textAlign': 'center', 'fontSize': 18}
    )