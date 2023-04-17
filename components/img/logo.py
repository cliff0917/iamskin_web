import dash_bootstrap_components as dbc
from dash import html

def serve():
    return html.A(
        # 利用 row, col 來控制排版
        dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src="./assets/common/img/logo.png", 
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