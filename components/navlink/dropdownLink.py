import dash_bootstrap_components as dbc

def serve(text, link):
    return dbc.DropdownMenuItem(
        text, external_link=True, href=link, 
        style={'textAlign': 'center', 'fontSize': 18}
    )