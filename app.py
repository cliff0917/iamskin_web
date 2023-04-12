import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import webbrowser
import dash_uploader as du

import globals
from utils import service
from lib import api, layout, download

app = dash.Dash(__name__, suppress_callback_exceptions=True)

du.configure_upload(app, folder='assets/web/upload') # uploader 的儲存路徑

config = globals.read_json('config.json')

app.title = "愛美膚 iamSkin"
app._favicon = ("common/img/logo.png")
server = app.server
server.secret_key = config['domain_name']
server = api.serve(server)
app.layout = layout.serve # live update, 請注意這裡是要用 serve 而非 serve()

download.all(config) # 將下載的 model 放在 model_path 中
server = service.serve(server, config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, dev_tools_props_check=False, ssl_context='adhoc')