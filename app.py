import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import webbrowser
import dash_uploader as du

import globals
from api import service
from utils import login, layout, download, lineBot

app = dash.Dash(__name__, suppress_callback_exceptions=True)

du.configure_upload(app, folder='assets/web/upload') # uploader 的儲存路徑

config = globals.read_json('config.json')

# 從 google drive 下載所有 model 和 secret file
download.all_models(config)
download.secret_file(config)

# 設定 client_secret
client_secrets_file = config["google_drive"]["client_secret"]["file_path"]
secret_config = globals.read_json(client_secrets_file)

# web 設定
app.title = "愛美膚 iamSkin"
app._favicon = ("common/img/logo.png")
server = app.server
server.secret_key = config['domain_name']
server = login.serve(server, secret_config, client_secrets_file)
app.layout = layout.serve # live update, 請注意這裡是要用 serve 而非 serve()

# 提供 API
server = service.serve(server)

# 提供 linebot 服務
server = lineBot.serve(server, config, secret_config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, dev_tools_props_check=False, ssl_context='adhoc')