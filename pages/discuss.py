import dash
import feffery_antd_components as fac
from dash import dcc, html, callback
from flask import session
from dash.dependencies import Input, Output, MATCH

import globals
from components import discuss_comment

def serve_layout():
    if session.get("type", None) == None:
        default_tab = 'Skin'
    else:
        default_tab = session["type"]

    return dcc.Loading(
        html.Div(
            [
                fac.AntdTitle('討論區', level=1),
                fac.AntdTabs(
                    [
                        fac.AntdTabPane(
                            discuss_comment.serve('Skin'),
                            tab='膚質 Skin',
                            key='Skin'
                        ),
                        fac.AntdTabPane(    
                            discuss_comment.serve('Nail'),
                            tab='指甲 Nail',
                            key='Nail'
                        ),
                        fac.AntdTabPane(    
                            discuss_comment.serve('Acne'),
                            tab='痘痘 Acne',
                            key='Acne'
                        ),
                    ],
                    type='card',
                    tabPaneAnimated=True,
                    defaultActiveKey=default_tab
                )
            ]
        )
    )
    