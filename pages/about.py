import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import html

import globals

def serve_layout():
    layout = html.Div(
        [
            html.H1(
                '關於我們',
                style={
                    'font-weight': 'bold',
                },
            ),
            html.Hr(),
            html.H3('▪ Line 官方帳號：'),
            fac.AntdImage(
                src=f"{globals.config['img_path']}/qrcode.png",
                style={
                    'height': "40%",
                    'padding': '1rem 1rem',
                },
                locale='en-us'
            ),
            dbc.Row(
                [
                    html.H3('▪ 聯絡資訊：'),
                    html.A(
                        html.H3(
                            'iamskin.uscc@gmail.com',
                            style={
                                'color': "#00B0F0", 
                                'text-decoration': 'underline',
                            }
                        ),
                        href='mailto:iamskin.uscc@gmail.com?subject=Feedback&body=愛美膚使用回饋'
                    )
                ],
                style={
                    'margin-left': '1.5px',
                },
            )
        ],
    )
    return layout