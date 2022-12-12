import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import webbrowser
from flask import request
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from flask import send_from_directory

import globals
from components import navbar, sidebar
from pages import home, about, skin, nail, acne, common_questions, non_exist

app = dash.Dash(__name__, suppress_callback_exceptions=True)
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

@app.server.route('/upload/', methods=['POST'])
def upload():
    # 获取上传id参数，用于指向保存路径
    uploadId = request.values.get('uploadId')

    # 获取上传的文件名称
    filename = request.files['file'].filename

    # 基于上传id，若本地不存在则会自动创建目录
    try:
        os.mkdir(os.path.join('upload', uploadId))
    except FileExistsError:
        pass

    # 流式写出文件到指定目录
    with open(os.path.join('upload', uploadId, filename), 'wb') as f:
        # 流式写出大型文件，这里的10代表10MB
        for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
            f.write(chunk)

    return {'filename': filename}

if __name__ == '__main__':
    debug = 1

    if debug == 1:
        # app.run(host='0.0.0.0', port=8080, debug=True, dev_tools_props_check=False, ssl_context='adhoc')
        app.run(host='0.0.0.0', port=8080, debug=True, dev_tools_props_check=False)
    else:
        pid = os.fork()
        if pid != 0:
            app.run_server()
        else:
            url = "http://127.0.0.1:8050/"
            webbrowser.open(url)