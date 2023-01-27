import dash_bootstrap_components as dbc
from dash import html

import globals

def serve():
    logo = html.A(
        # 利用 row, col 來控制排版
        dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src=f"{globals.config['assets_path']}/common/img/logo.png", 
                        height="50px",
                    )
                ),
            ],
            align="center",
            className="g-0",
        ),
        href="/",
        style={"textDecoration": "none"},
    )
    return logo