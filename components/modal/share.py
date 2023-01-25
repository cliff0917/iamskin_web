import dash
import feffery_antd_components as fac
from dash import callback
from flask import session
from dash.dependencies import Input, Output, State, MATCH

import globals
import database
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
    # insert data 到 db
    if checked == True:
        img_path = session["output_path"]
    else:
        img_path = ''
        
    database.insert(
        session["google_id"],
        session["name"],
        session["email"],
        session["locale"],
        session["cur_path"][1:],
        globals.now(),
        rate,
        comment,
        img_path
    )
    return dash.no_update