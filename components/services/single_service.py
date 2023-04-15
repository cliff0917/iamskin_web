import feffery_antd_components as fac
import dash_bootstrap_components as dbc
from dash import html

from components.services import paragraph

def serve(service_type, chinese):
    return dbc.Col(
        [
            fac.AntdImage(
                src=f"./assets/{service_type}/img/icon.png",
                preview=False,
                style={
                    'height': '130px',
                }
            ),
            html.H3(
                f'{chinese}檢測 - {service_type}',
                style={
                    'color': '#7891AA',
                    'font-weight': 'bold',
                },
            ),
            html.Hr(style={'margin-left': '2rem', 'margin-right': '2rem'}),
            paragraph.serve(service_type),
            dbc.Button(
                f"點擊分析{chinese}",
                color="primary",
                outline=True,
                external_link=True,
                href=f'/{service_type}',
                style={
                    'font-weight': 'bold',
                },
                size='lg',
            ),
        ],
        style={
            'background-color': '#F7F7F8',
            'textAlign': 'center',
            'padding': '2rem',
            'margin-left': '1rem',
            'margin-right': '1rem',
            'margin-bottom': '1rem',
        },
    )