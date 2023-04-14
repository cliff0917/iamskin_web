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
                            comments.serve(key),
                            tab=f'{value["normal"]} {key}',
                            key=key
                        )
                        for key, value in globals.config["chinese"].items() # 用 config 初始化討論區種類
                    ],
                    type='card',
                    tabPaneAnimated=True,
                    defaultActiveKey=default_tab
                ),
            ),
        ]
    )