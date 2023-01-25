import dash_bootstrap_components as dbc

def serve(text, link):
    return dbc.NavItem(
        dbc.NavLink(
            text, external_link=True, href=link, 
            style={"color": "black"}
        ), 
        style={'textAlign': 'center'}
    )