from dash import html
import feffery_antd_components as fac

from components import user_history

def serve_layout():
    return html.Div(
        [
            fac.AntdTitle('歷史紀錄', level=1),
            user_history.serve()
        ]
    )