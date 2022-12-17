import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import webbrowser
from dash import dcc, html, callback
from dash.dependencies import Input, Output

import globals
from lib import login, upload
from components import navbar, sidebar
from pages import home, about, prediction, common_questions, non_exist

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.title = "愛美膚 iamSkin"
app._favicon = ("img/logo.png")
server = app.server
server.secret_key = "iamskin.tk"
server = login.serve(server)
server = upload.serve(server)

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
        ],
    )
    return layout

# live update, 請注意這裡是要用 serve_layout 而非 serve_layout()
app.layout = serve_layout

# 透過 url 來決定顯示哪個 page
@callback(
    Output('content', 'children'),
    Input('url', 'pathname'),
)
def display_page(pathname):
    # live update layout
    if pathname in ['/', '/Home']:
        return home.serve_layout()

    elif pathname == '/About-us':
        return about.serve_layout()

    elif pathname in ['/Skin', '/Nail', '/Acne']:
        return prediction.serve_layout(
            pathname[1:], # 哪種 type
            True,
        )

    elif pathname == '/Q&A':
        return common_questions.serve_layout()

    return non_exist.serve_layout()  # 若非以上路徑, 則 return 404 message

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
            webbrowser.open(url)