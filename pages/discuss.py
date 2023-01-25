import dash
import feffery_antd_components as fac
from dash import dcc, html, callback
from flask import session
from dash.dependencies import Input, Output, MATCH

import globals
from components import comments

def serve_layout():
    if session.get("type", None) == None:
        default_tab = 'Skin'
    else:
        default_tab = session["type"]

    return html.Div(
        [
            fac.AntdTitle('討論區', level=1),
            dcc.Loading(
                fac.AntdTabs(
                    [
                        fac.AntdTabPane(
                            comments.serve('Skin'),
                            tab='膚質 Skin',
                            key='Skin'
                        ),
                        fac.AntdTabPane(    
                            comments.serve('Nail'),
                            tab='指甲 Nail',
                            key='Nail'
                        ),
                        fac.AntdTabPane(    
                            comments.serve('Acne'),
                            tab='痘痘 Acne',
                            key='Acne'
                        ),
                    ],
                    type='card',
                    tabPaneAnimated=True,
                    defaultActiveKey=default_tab
                ),
            ),
        ]
    )