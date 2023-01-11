from dash import html
import feffery_antd_components as fac

def serve_layout():
    return html.Div(
        [
            fac.AntdResult(
                status='404',
                title=fac.AntdTitle(
                    '404 錯誤：此網頁不存在',
                    level=4,
                ),
            )
        ]
    )