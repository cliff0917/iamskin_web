import dash_bootstrap_components as dbc
from dash import html

import globals
from components.services import single_service

def serve():
    services = html.Div(
        dbc.Row(
            [
                single_service.serve(key, value["tutorial"])
                for key, value in globals.config["chinese_mapping"].items() # 利用 config 初始化 tutorial
            ]
        )
    )
    return services