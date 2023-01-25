import dash
import dash_bootstrap_components as dbc
from dash import callback
from flask import session
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac

import globals
from components import logo, modal, logout

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
                            logout.serve(),
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
                modal.serve('login', '登入帳號', '使用 Google 繼續', '/login'),
            ],
            fluid=True,
        ),
        color="#8EA0A5",
        sticky='top',
    )
    return navbar


@callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
    prevent_initial_call=True
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open