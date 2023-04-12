import dash
import feffery_antd_components as fac
from flask import session
from datetime import datetime
from dash import callback
from dash.dependencies import Input, Output, MATCH

import globals
from components.tab import comment, preview
from components.img import comment_attach

def serve(service_type):
    return fac.AntdTabs(
        [
            comment.serve(service_type),
            preview.serve(service_type),
        ]
    )

@callback(
    [
        Output({'type': 'comment', 'index': MATCH}, 'value'),
        Output({'type': 'preview-time', 'index': MATCH}, 'children'),
        Output({'type': 'preview-rate', 'index': MATCH}, 'value'),
        Output({'type': 'preview-comment-title', 'index': MATCH}, 'children'),
        Output({'type': 'preview-comment', 'index': MATCH}, 'children'),
        Output({'type': 'preview-img-collapse', 'index': MATCH}, 'is_open'),
        Output({'type': 'preview-img-collapse', 'index': MATCH}, 'children'),
    ],
    [
        Input({'type': 'rate', 'index': MATCH}, 'value'),
        Input({'type': 'comment', 'index': MATCH}, 'value'),
        Input({'type': 'img-switch', 'index': MATCH}, 'checked'),
    ],
    prevent_initial_call=True
)
def update_comment(value, comment, checked):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split('.')[0]
    triggered_id = triggered_id.split('"')[-2]
    # print(triggered_id)

    # 變動的是 rate
    if triggered_id == 'rate':
        comment = globals.rate_text[value - 1]
        return [
            comment, globals.now(), value, '評論：',
            comment, dash.no_update, dash.no_update
        ]

    # 變動的是 comment
    elif triggered_id == 'comment':
        if comment == '':
            return [
                dash.no_update, globals.now(), dash.no_update, 
                '', comment, dash.no_update, dash.no_update
            ]

        return [
            dash.no_update, globals.now(), dash.no_update, 
            '評論：', comment, dash.no_update, dash.no_update
        ]

    # 變動的是 img-switch
    else:
        if checked:
            img = comment_attach.serve(session["output_path"], '100%')
            return [
                dash.no_update, globals.now(), dash.no_update, 
                dash.no_update, dash.no_update, True, img
            ]
        return [
            dash.no_update, globals.now(), dash.no_update, 
            dash.no_update, dash.no_update, False, dash.no_update
        ]