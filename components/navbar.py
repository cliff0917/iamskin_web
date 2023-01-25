import dash
import dash_bootstrap_components as dbc
from dash import callback
from flask import session
from dash.dependencies import Input, Output, State

import globals
from components import logo, navbar_btn, modal

def serve():
    navbar = dbc.Navbar(
        dbc.Container(
            [
                logo.serve(),
                dbc.NavbarToggler(
                    id="navbar-toggler", 
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("首頁", href="/Home", style={"color": "black"}), style={'textAlign': 'center'}),
                            dbc.NavItem(dbc.NavLink("關於我們", href="/About-us", style={"color": "black"}), style={'textAlign': 'center'}),
                            dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem("膚質檢測", href="/Skin", style={'textAlign': 'center'}),
                                    dbc.DropdownMenuItem("指甲檢測", href="/Nail", style={'textAlign': 'center'}),
                                    dbc.DropdownMenuItem("痘痘檢測", href="/Acne", style={'textAlign': 'center'}),
                                ],
                                nav=True,
                                in_navbar=True,
                                label="服務項目",
                                toggle_style={"color": "black"},
                                style={'textAlign': 'center'}
                            ),
                            dbc.NavItem(dbc.NavLink("討論區", href="/Discuss", style={"color": "black"}), style={'textAlign': 'center'}),
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
                modal.serve('login', '登入帳號', '使用 Google 繼續', '/login'),
                modal.serve('logout', '登出帳號', '登出', '/', False),
            ],
            fluid=True,
        ),
        color="#8EA0A5",
        sticky='top',
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

@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open