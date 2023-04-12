import feffery_antd_components as fac
import dash_bootstrap_components as dbc
from dash import html

import globals

def serve(service_type):
    tutorial = fac.AntdPopover(
        dbc.Button(
            '使用說明',
            color="primary",
            outline=True,
            style={
                'margin-top': '1rem',
            }
        ),
        title='使用說明',
        content=fac.AntdParagraph(
            [
                fac.AntdText('照片要確實含有您的'),
                fac.AntdText(f"{globals.config['chinese'][service_type]['tutorial']}", code=True),
                fac.AntdText('且盡量有充足光源，並注意不要'),
                fac.AntdText('失焦', code=True),
                fac.AntdText('，否則判讀結果不具任何意義。'),
                html.Br(),
                html.Br(),
                fac.AntdText('請參考下方範例圖片來上傳'),
                fac.AntdText(f"{globals.config['chinese'][service_type]['tutorial']}", code=True),
                fac.AntdText('圖片，即可得到結果。'),
                html.Br(),
                html.Br(),
                fac.AntdImage(
                    src=f"./assets/{service_type}/img/example.png",
                    preview=False,
                ),
            ]
        ),
        placement='left',
    )
    return tutorial