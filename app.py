import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import webbrowser
import dash_uploader as du

import globals, download
from utils import login, layout, service

app = dash.Dash(__name__, suppress_callback_exceptions=True)

du.configure_upload(app, folder='assets/upload') # uploader 的儲存路徑

app.title = "愛美膚 iamSkin"
app._favicon = ("common/img/logo.png")
server = app.server
server.secret_key = "iamskin.tk"
server = login.serve(server)
app.layout = layout.serve # live update, 請注意這裡是要用 serve 而非 serve()

config = globals.read_json('config.json')
download.all(config) # 將下載的 model 放在 model_path 中
server = service.serve(server, config)

if __name__ == '__main__':
    pid = os.fork()
    if pid != 0:
        app.run(host='0.0.0.0', port=8080, dev_tools_props_check=False, ssl_context='adhoc')
    else:
        url = "https://iamskin.tk/"