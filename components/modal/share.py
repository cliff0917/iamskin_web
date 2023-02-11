import dash
import feffery_antd_components as fac
from dash import callback
from flask import session
from dash.dependencies import Input, Output, State, MATCH

import globals, database
from components.tab import share

def serve(types):
    return fac.AntdModal(
        visible=False,
        title=share.serve(types),
        renderFooter=True,
        okText='送出',
        okCounts=0,
        cancelText='取消',
        okButtonProps={
            'href': '/Discuss'
        },
        id={
            'type': 'share-modal',
            'index': types
        },
    )


@callback(
    Output({'type': 'share-modal', 'index': MATCH}, 'renderFooter'),
    Input({'type': 'share-modal', 'index': MATCH}, 'okCounts'),
    [
        State({'type': 'preview-rate', 'index': MATCH}, 'value'),
        State({'type': 'preview-comment', 'index': MATCH}, 'children'),
        State({'type': 'img-switch', 'index': MATCH}, 'checked'),
    ],
    prevent_initial_call=True,
)
def insert_data(okCounts, rate, comment, checked):
    # 若要分享, 則更新 history 中的 display_output, publish_time, rate, comment
    if checked == True:
        display_output_img = 1
    else:
        display_output_img = 0

    info = (
        display_output_img, globals.now(), rate, comment, 
        session["google_id"], session["cur_path"][1:], session["input_path"]
    )
    database.update_history(info)
    return dash.no_update