import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import base64
import requests
import webbrowser
from flask import request
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from flask import send_from_directory

import globals
from transfer import encode
from components import navbar, sidebar
from pages import home, about, skin, nail, acne, common_questions, non_exist

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.title = "愛美膚 iamSkin"
app._favicon = ("img/logo.png")

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
    Input('url', 'pathname')
)
def display_page(pathname):
    # live update layout
    if pathname in ['/', '/Home']:
        return home.serve_layout()

    elif pathname == '/About-us':
        return about.serve_layout()

    elif pathname == '/AI-Prediction/Skin':
        return skin.serve_layout()

    elif pathname == '/AI-Prediction/Nail':
        return nail.serve_layout()

    elif pathname == '/AI-Prediction/Acne':
        return acne.serve_layout()

    elif pathname == '/Q&A':
        return common_questions.serve_layout()

    return non_exist.serve_layout()  # 若非以上路徑, 則 return 404 message

@server.route('/upload/', methods=['POST'])
def upload():
    # 獲取上傳 id, 指向 save path
    uploadId = request.values.get('uploadId')

    # 獲取上傳檔案名稱
    filename = request.files['file'].filename

    # 建立上傳 id 的目錄
    try:
        os.mkdir(os.path.join('upload', uploadId))
    except FileExistsError:
        pass

    filepath = os.path.join('upload', uploadId, filename)

    # 將檔案寫到指定目錄
    with open(filepath, 'wb') as f:
        # 每次讀 10 MB
        for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
            f.write(chunk)

    with open(filepath, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())

    response = requests.post(
        'http://0.0.0.0:9487/skin-classifier',
        json={
            'format': 'flask',
            'image': b64_string.decode('ascii'),
        }
    )
    response = response.json()

    return {'filename': filename}

if __name__ == '__main__':
    debug = 1

    if debug == 1:
        # app.run(host='0.0.0.0', port=8080, dev_tools_props_check=False, ssl_context='adhoc')
        app.run(host='0.0.0.0', port=8050, debug=True, dev_tools_props_check=False)
    else:
        pid = os.fork()
        if pid != 0:
            app.run_server()
        else:
            url = "http://127.0.0.1:8050/"
            webbrowser.open(url)