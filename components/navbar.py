from dash import html
import dash_bootstrap_components as dbc

import globals

def serve():
    navbar = dbc.Navbar(
        [
            html.A(
                # 利用 row, col 來控制排版
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=f"{globals.config['img_path']}/logo.png", height="50px"))
                    ],
                ),
                href="https://iamskin.tk/",
            ),
            # dbc.Col(style={'width': 4}),
            # html.A(
            #     # 利用 row, col 來控制排版
            #     dbc.Row(
            #         dbc.Col(html.Img(className="github", src=github, height="50px")),
            #     ),
            #     href="https://github.com/cliff0917/dashboard",
            # ),
        ],
        # color="#F5F5F5",
        color="#8EA0A5",
        sticky='top',
        style={
            'width':'100%',
            'height':'80px',
        },
    )
    return navbar