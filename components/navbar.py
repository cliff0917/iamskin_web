import dash_bootstrap_components as dbc
from dash import callback
from flask import session
from dash.dependencies import Input, Output, State

import globals
from components.navlink import navItem, logout, dropdownLink
from components.img import logo

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
                            navItem.serve("首頁", '/'),
                            navItem.serve("關於我們", '/About'),
                            dbc.DropdownMenu(
                                children=[
                                    dropdownLink.serve("膚質檢測", "/Skin"),
                                    dropdownLink.serve("指甲檢測", "/Nail"),
                                    dropdownLink.serve("痘痘檢測", "/Acne"),
                                ],
                                nav=True,
                                in_navbar=True,
                                label="服務項目",
                                toggle_style={"color": "black"},
                                id='nav-dropdown-title',
                                style={'textAlign': 'center'}
                            ),
                            navItem.serve("討論區", '/Discuss'),
                            navItem.serve("歷史紀錄", '/History'),
                            logout.serve(),
                        ],
                        className='ml-auto', # navlink 向右對齊
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                    style={"fontSize": 18}
                ),
            ],
            fluid=True,
        ),
        # color="#8EA0A5",
        color='white',
        sticky='top',
        style={'border-bottom': '1px #E3E3E4 solid'}
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