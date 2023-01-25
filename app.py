import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import webbrowser
import dash_uploader as du
from flask import session
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State

import globals
from utils import login, upload
from components import navbar, modal
from components.modal import social_login
from pages import home, about, prediction, discuss, policy, non_exist

app = dash.Dash(__name__, suppress_callback_exceptions=True)

du.configure_upload(app, folder='assets/upload') # uploader 的儲存路徑

app.title = "愛美膚 iamSkin"
app._favicon = ("img/logo.png")
server = app.server
server.secret_key = "iamskin.tk"
server = login.serve(server)

# components
url = dcc.Location(id="url")

content = html.Div(
    id='content', 
    style={
        'padding': '2rem 2rem', 
    }
)

def serve_layout():
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

# live update, 請注意這裡是要用 serve_layout 而非 serve_layout()
app.layout = serve_layout

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

    # live update layout
    if pathname == '/':
        return [home.serve_layout(), False, {'color': 'black'}]

    elif pathname == '/About':
        return [about.serve_layout(), False, {'color': 'black'}]

    elif pathname in globals.services:
        # 如果未登入帳號, 則跳出 login first modal
        if session.get("google_id", None) == None:
            return [dash.no_update, True, {'color': 'blue'}]

        return [
            prediction.serve_layout(
                pathname[1:], # 哪種 type
                True,
            ),
            False,
            {'color': 'blue'}
        ]

    elif pathname == '/Discuss':
        return [discuss.serve_layout(), False, {'color': 'black'}]

    elif pathname == '/terms':
        return [policy.serve_layout('服務條款'), False, {'color': 'black'}]

    elif pathname == '/privacy-policy':
        return [policy.serve_layout('隱私權政策'), False, {'color': 'black'}]

    return [non_exist.serve_layout(), False, {'color': 'black'}]  # 若非以上路徑, 則顯示 404


if __name__ == '__main__':
    debug = 0

    if debug == 1:
        app.run(host='0.0.0.0', port=8080, debug=True, dev_tools_props_check=False)
    else:
        pid = os.fork()
        if pid != 0:
            app.run(host='0.0.0.0', port=8080, dev_tools_props_check=False, ssl_context='adhoc')
        else:
            url = "https://iamskin.tk/"
            # webbrowser.open(url)