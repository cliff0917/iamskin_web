import feffery_antd_components as fac
import dash_bootstrap_components as dbc
from dash import html

import globals
from components import paragraph

def serve():
    services = dbc.Row(
        [
            dbc.Col(
                [
                    fac.AntdImage(
                        src=f"{globals.config['img_path']}/skin.png",
                        preview=False,
                        style={
                            'height': '130px',
                        }
                    ),
                    html.H3(
                        '膚質大師 - SkinTest',
                        style={
                            'color': '#7891AA',
                            'font-weight': 'bold',
                        },
                    ),
                    html.Hr(),
                    paragraph.serve('skin'),
                    dbc.Button(
                        "點擊分析膚質",
                        color="primary",
                        outline=True,
                        href='/Skin-Prediction',
                        style={
                            'font-weight': 'bold',
                        },
                        size='lg',
                    ),
                    html.P(''),
                ],
                style={
                    'background-color': '#FFFFFF',
                    'textAlign': 'center',
                    'margin-right': '2rem',
                },
            ),
            dbc.Col(
                [
                    fac.AntdImage(
                        src=f"{globals.config['img_path']}/nail.png",
                        preview=False,
                        style={
                            'height': '130px',
                        }
                    ),
                    html.H3(
                        '指甲大師 - NailTest',
                        style={
                            'color': '#7891AA',
                            'font-weight': 'bold',
                        },
                    ),
                    html.Hr(),
                    paragraph.serve('nail'),
                    dbc.Button(
                        "點擊分析指甲",
                        color="primary",
                        outline=True,
                        href='/Nail-Prediction',
                        style={
                            'font-weight': 'bold',
                        },
                        size='lg',
                    ),
                    html.P(''),
                ],
                style={
                    'background-color': '#FFFFFF',
                    'textAlign': 'center',
                    'margin-right': '2rem',
                },
            ),
            dbc.Col(
                [
                    fac.AntdImage(
                        src=f"{globals.config['img_path']}/acne.png",
                        preview=False,
                        style={
                            'height': '130px',
                        }
                    ),
                    html.H3(
                        '痘痘大師 - AcneTest',
                        style={
                            'color': '#7891AA',
                            'font-weight': 'bold',
                        },
                    ),
                    html.Hr(),
                    paragraph.serve('acne'),
                    dbc.Button(
                        "點擊分析痘痘",
                        color="primary",
                        outline=True,
                        href='/Acne-Prediction',
                        style={
                            'font-weight': 'bold',
                        },
                        size='lg',
                    ),
                    html.P(''),
                ],
                style={
                    'background-color': '#FFFFFF',
                    'textAlign': 'center',
                },
            ),
        ],
        style={
            "padding": "2rem 1rem",
        },
    )
    return services