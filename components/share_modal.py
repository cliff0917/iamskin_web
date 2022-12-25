import feffery_antd_components as fac
from dash import dcc, html, callback

import globals
from components import tab

def serve(types):
    return fac.AntdModal(
        visible=False,
        title=tab.serve(types),
        renderFooter=True,
        okText='送出',
        cancelText='取消',
        id={
            'type': 'share-modal',
            'index': types
        },
    )