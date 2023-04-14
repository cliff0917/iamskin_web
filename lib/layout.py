import dash
from flask import session
from dash import dcc, html, callback
from dash.dependencies import Input, Output

import globals
from components.modal import social_login
from components import navbar, modal
from pages import home, about, services, comments, history, policy, non_exist
from components.common_style import navlink_active, navlink_not_active

url = dcc.Location(id="url")

content = html.Div(
    id='content', 
    style={
        'padding': '2rem 2rem', 
    }
)

def serve():
    # 得到最新狀態的 db
    globals.initialize()

    layout = html.Div(
        [
            url,
            navbar.serve(),
            content,
            social_login.serve(
                'login-first',
                '請先登入帳號',
                '使用 Google 繼續',
                '/login'
            ),
        ],
        style={'font-family': 'Microsoft YaHei UI', 'color': 'black'}
    )
    return layout


# 透過 url 來決定顯示哪個 page
@callback(
    [
        Output('content', 'children'),
        Output('login-first-modal', 'visible'),
        Output('nav-dropdown-title', 'toggle_style'), # 服務項目的顏色 
    ],
    Input('url', 'pathname'),
    prevent_initial_call=True
)
def display_page(pathname):
    session["cur_path"] = pathname
    dropdown_navlink = navlink_not_active

    # live update layout
    if pathname == '/':
        return [home.serve_layout(), False, dropdown_navlink]

    elif pathname == '/About':
        return [about.serve_layout(), False, dropdown_navlink]

    elif pathname in globals.services:
        dropdown_navlink = navlink_active

        # 如果未登入帳號, 則跳出 login first modal
        if session.get("google_id", None) == None:
            return [dash.no_update, True, dropdown_navlink]
            
        return [
            services.serve_layout(
                pathname[1:], # 哪種 type
                True,
            ),
            False,
            dropdown_navlink
        ]

    elif pathname == '/Comments':
        return [comments.serve_layout(), False, dropdown_navlink]

    elif pathname == '/History':
        # 如果未登入帳號, 則跳出 login first modal
        if session.get("google_id", None) == None:
            return [dash.no_update, True, dropdown_navlink]
            
        return [history.serve_layout(), False, dropdown_navlink]

    elif pathname == '/terms-of-use':
        return [policy.serve_layout('服務條款'), False, dropdown_navlink]

    elif pathname == '/privacy-policy':
        return [policy.serve_layout('隱私權政策'), False, dropdown_navlink]

    return [non_exist.serve_layout(), False, dropdown_navlink]  # 若非以上路徑, 則顯示 404