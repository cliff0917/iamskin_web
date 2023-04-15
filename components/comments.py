from dash import html
import dash_bootstrap_components as dbc
import feffery_antd_components as fac

import globals
from components import bold_text
from components.img import comment_attach
from lib import database

def serve(service_type):
    comments = []
    type_comments = database.get_comments(service_type)

    if len(type_comments) == 0:
        return fac.AntdEmpty(
            description=bold_text.serve('暫無評論')
        )
    
    # 新的 comment 會顯示在較上面
    for type_comment in type_comments[::-1]:
        comment_section, img = None, None
        uid, name, upload_time, file_name, predict_class, display_output_img, publish_time, rate, comment = type_comment

        if comment != '':
            comment_section = html.Div(
                [
                    fac.AntdText(
                        '評論：',
                        style={
                            'font-weight': 'bold',
                        },
                    ),
                    fac.AntdText(comment)
                ],
                style={
                    'margin-top': '5px',
                    'margin-left': '1rem',
                }
            )

        if display_output_img == 1:
            img = comment_attach.serve(f'assets/{service_type}/img/{predict_class}.png', '306px')

        single_comment = html.Div(
            [
                fac.AntdAvatar(
                    mode='icon',
                    size='xs',
                    style={
                        'backgroundColor': 'rgb(16, 105, 246)'
                    }
                ),
                fac.AntdText(
                    f'{name[0]}{"*" * 5}{name[-1]}',
                    style={
                        'margin-left': '5px',
                    }
                ),
                fac.AntdText(
                    publish_time,
                    type='secondary',
                    style={
                        'margin-left': '1rem',
                    },
                ),
                html.Br(),
                fac.AntdText(
                    f'檢測類別：{globals.config["chinese"][service_type]["normal"]}',
                    style={
                        'margin-left': '1rem',
                        'font-weight': 'bold',
                    },
                ),
                html.Br(),
                fac.AntdText(
                    '評分：',
                    style={
                        'margin-left': '1rem',
                        'font-weight': 'bold',
                    },
                ),
                fac.AntdRate(
                    count=5,
                    defaultValue=rate,
                    disabled=True,
                ),
                html.Br(),
                comment_section,
                img,
                html.Hr()
            ],
            style={
                'background-color': '#F7F7F8'
            }
        )
        comments.append(single_comment)

    return html.Div(comments)