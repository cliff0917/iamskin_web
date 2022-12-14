import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import base64
import pathlib
import requests
import webbrowser
from flask import request
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from flask import send_from_directory, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

import globals
from transfer import encode
from components import navbar, sidebar
from pages import home, about, skin, nail, acne, common_questions, non_exist

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, 'client_secret.json')
client_secrets = globals.read_json(client_secrets_file)
GOOGLE_CLIENT_ID = client_secrets["web"]["client_id"]

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri=client_secrets["web"]["redirect_uris"][0]
)

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.title = "愛美膚 iamSkin"
app._favicon = ("img/logo.png")
server.secret_key = "iamskin.tk"

# components
url = dcc.Location(id="url")

def serve_layout():
    # 得到最新狀態的 db
    globals.initialize()

    layout = html.Div(
        [
            url,
            navbar.serve(session),
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

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper

@server.route("/protected_area")
@login_is_required
def protected_area():
    return f"{session}"

@server.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@server.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["picture"] = id_info.get("picture")
    return redirect("/")



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