import dash
import dash_bootstrap_components as dbc
from dash import callback
from flask import session
from dash.dependencies import Input, Output

import globals
from components import logo, navbar_btn, modal

def serve(session):
    navbar = dbc.Navbar(
        [
            logo.serve(),
            dbc.Col(
                style={
                    'width': 4,
                }
            ),
            navbar_btn.serve(session),
            modal.serve('login', '登入帳號', '使用 Google 繼續', '/login'),
            modal.serve('logout', '登出帳號', '登出', '/'),
        ],
        color="#8EA0A5",
        sticky='top',
        style={
            'width':'100%',
            'height':'80px',
        },
    )
    return navbar

# 點擊 navbar 上的登入按鈕, 跳出登入 Google 帳號的 modal
@callback(
    Output('login-modal', 'visible'),
    Input('login-btn', 'nClicks'),
    prevent_initial_call=True
)
def login_modal(nClicks):
    return True

# 點擊 navbar 上 avatar, 跳出登出 Google 帳號的 modal
@callback(
    Output('logout-modal', 'visible'),
    Input('avatar', 'nClicks'),
    prevent_initial_call=True
)
def logout_modal(nClicks):
    return True

# 點擊 Google 登出按鈕, 清空 cookie
@callback(
    Output('avatar', 'shape'),
    Input('google-logout-btn', 'nClicks'),
    prevent_initial_call=True
)
def click(nClicks):
    session.clear()
    return dash.no_update