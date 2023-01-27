import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import html

import globals

def serve_layout():
    layout = html.Div(
        [
            fac.AntdTitle('關於我們', level=1),
            html.Hr(),
            html.H3('▪ Line 官方帳號'),
            dbc.Row(
                [
                    html.H4('▪ 網址：'),
                    html.A(
                        html.H4(
                            'https://line.me/R/ti/p/@627kkxpf',
                            style={
                                'color': "#00B0F0", 
                                'text-decoration': 'underline',
                            }
                        ),
                        href='https://line.me/R/ti/p/@627kkxpf'
                    ),
                ],
                style={'margin-left': '2rem'},
            ),
            html.H4('▪ QR Code：', style={'margin-left': '2rem'}),
            fac.AntdImage(
                src=f"{globals.config['assets_path']}/common/img/qrcode.png",
                style={
                    'height': "40%",
                    'padding': '0rem 1rem',
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