from dash import html
import feffery_antd_components as fac

import globals
from components import bold_text

def serve(types):
    return fac.AntdTabPane(
        [
            bold_text.serve(
                f'檢測類別：{globals.config["service_intro"][types]["title"][:2]}',
            ),
            html.Br(),
            bold_text.serve('評分：'),
            fac.AntdRate(
                count=5,
                tooltips=globals.rate_text,
                defaultValue=3,
                id={
                    'type': 'rate',
                    'index': types
                },
            ),
            html.Div(
                [
                    bold_text.serve('結果圖：'),
                    fac.AntdSwitch(
                        checkedChildren='分享',
                        unCheckedChildren='不分享',
                        checked=False,
                        id={
                            'type': 'img-switch',
                            'index': types
                        },
                    ),
                ],
                style={
                    'margin-top': '5px',
                }
            ),
            fac.AntdInput(
                mode='text-area',
                placeholder='使用感想',
                style={
                    'margin-top': '10px',
                    'height': '80px'
                },
                id={
                    'type': 'comment',
                    'index': types
                },
            ),
        ],
        tab='撰寫評論',
        key='撰寫評論'
    )