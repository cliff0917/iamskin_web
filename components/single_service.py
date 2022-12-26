import feffery_antd_components as fac
import dash_bootstrap_components as dbc
from dash import html

import globals
from components import paragraph

# last 代表是否為該列最後一個元素
def serve(chinese, types, last):
    return dbc.Col(
        [
            fac.AntdImage(
                src=f"{globals.config['img_path']}/{types}/icon.png",
                preview=False,
                style={
                    'height': '130px',
                }
            ),
            html.H3(
                f'{chinese}大師 - {types}Test',
                style={
                    'color': '#7891AA',
                    'font-weight': 'bold',
                },
            ),
            html.Hr(),
            paragraph.serve(types),
            dbc.Button(
                f"點擊分析{chinese}",
                color="primary",
                outline=True,
                href=f'/{types}',
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
            'margin-right': '2rem' if last != True else None,
        },
    )