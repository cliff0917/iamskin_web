import dash_bootstrap_components as dbc
from dash import html, callback
from flask import session
from dash.dependencies import Input, Output, State

import globals
from components import logo, modal, navItem, logout

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
                            navItem.serve("首頁", '/Home'),
                            navItem.serve("關於我們", '/About-us'),
                            dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem("膚質檢測", external_link=True, href="/Skin", style={'textAlign': 'center'}),
                                    dbc.DropdownMenuItem("指甲檢測", external_link=True, href="/Nail", style={'textAlign': 'center'}),
                                    dbc.DropdownMenuItem("痘痘檢測", external_link=True, href="/Acne", style={'textAlign': 'center'}),
                                ],
                                nav=True,
                                in_navbar=True,
                                label="服務項目",
                                toggle_style={"color": "black"},
                                style={'textAlign': 'center'}
                            ),
                            navItem.serve("討論區", '/Discuss'),
                            logout.serve(),
                        ],
                        className='ml-auto', # navlink 向右對齊
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
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