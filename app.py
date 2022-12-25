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
from components import navbar, sidebar, modal
from pages import home, about, prediction, faq, non_exist

app = dash.Dash(__name__, suppress_callback_exceptions=True)

du.configure_upload(app, folder='assets/upload')

app.title = "愛美膚 iamSkin"
app._favicon = ("img/logo.png")
server = app.server
server.secret_key = "iamskin.tk"
server = login.serve(server)

# components
url = dcc.Location(id="url")

def serve_layout():
    # 得到最新狀態的 db
    globals.initialize()

    layout = html.Div(
        [
            url,
            navbar.serve(),
            sidebar.serve(),
            modal.serve(
                'login-first',
                '請先登入帳號',
                '使用 Google 繼續',
                '/login'
            ),
        ],
    )
    return layout

# live update, 請注意這裡是要用 serve_layout 而非 serve_layout()
app.layout = serve_layout

# 透過 url 來決定顯示哪個 page
@callback(
    [
        Output('content', 'children'),
        Output('login-first-modal', 'visible'),
    ],
    Input('url', 'pathname'),
    prevent_initial_call=True
)
def display_page(pathname):
    session["cur_path"] = pathname

    # live update layout
    if pathname in ['/', '/Home']:
        return [home.serve_layout(), False]

    elif pathname == '/About-us':
        return [about.serve_layout(), False]

    elif pathname in globals.services:
        # 如果未登入帳號, 則跳出 login first modal
        # if session.get("google_id", None) == None:
        #     return [dash.no_update, True]

        return [
            prediction.serve_layout(
                pathname[1:], # 哪種 type
                True,
            ),
            False
        ]

    elif pathname == '/FAQ':
        return [faq.serve_layout(), False]

    return [non_exist.serve_layout(), False]  # 若非以上路徑, 則 return 404 message


# @callback(
#     Output('url', 'pathname'),
#     Input('login-first-modal', 'visible'),
#     prevent_initial_call=True
# )
# def close_modal(visible):
#     pathname = session.get('redirect', None)
#     user_id = session.get("google_id", None)

#     if visible == False and user_id == None and pathname in globals.services:
#         return '/'
#     return dash.no_update

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