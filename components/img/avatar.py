from flask import session
import feffery_antd_components as fac
import dash_bootstrap_components as dbc

def serve():
    return fac.AntdButton(
        fac.AntdAvatar(
            mode='image',
            src=session["picture"],
        ),
        type='link',
        style={'width': 47}
    )