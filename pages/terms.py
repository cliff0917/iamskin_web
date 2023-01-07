import dash
import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from flask import redirect

from components import terms_tab, privacy_policy_tab

def serve_layout(defaultActiveKey='服務條款'):
    return fac.AntdTabs(
        [
            terms_tab.serve(),
            privacy_policy_tab.serve(),
        ],
        defaultActiveKey=defaultActiveKey,
        id='policy'
    )

@callback(
    Output('url', 'pathname'),
    Input('policy', 'activeKey'),
    prevent_initial_call=True
)
def activate(activeKey):
    ctx = dash.callback_context
    if ctx.triggered[0]['value'] == '服務條款':
        return '/terms'
    return '/privacy-policy'