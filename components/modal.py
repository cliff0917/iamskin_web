import feffery_antd_components as fac
from dash import html

import globals

def serve(id, title, context, href=None):
    return fac.AntdModal(
        [
            html.A(
                fac.AntdRow(
                    fac.AntdCol(
                        fac.AntdButton(
                            [
                                html.Img(
                                    src=f"{globals.config['img_path']}/google-login.svg",
                                    height="27px",
                                    style={
                                        'margin-bottom': '3px',
                                    },
                                ),
                                html.A(
                                    context,
                                    style={
                                        'fontSize': 15,
                                        'font-weight': 'bold',
                                        'margin-left': '10px',
                                    },
                                ),
                            ],
                            nClicks=0,
                            style={
                                'height': '38px',
                            },
                            id=f'google-{id}-btn'
                        ),
                    ),
                    justify='center',
                ),
                href=href,
            )
        ],
        id=f'{id}-modal',
        visible=False,
        title=fac.AntdRow(
            fac.AntdCol(
                fac.AntdTitle(
                    title,
                    level=4,
                    style={
                        'justify': 'center',
                    },
                ),
            ),
            justify='center',
        ),
        renderFooter=False,
    )