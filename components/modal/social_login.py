import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import html

import globals

def serve(id, title, context, href=None, is_open=True):
    return fac.AntdModal(
        [
            html.A(
                fac.AntdRow(
                    fac.AntdCol(
                        fac.AntdButton(
                            [
                                html.Img(
                                    src=f"{globals.config['assets_path']}/common/img/google-login.svg",
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
            ),
            html.Br(),
            dbc.Collapse(
                fac.AntdRow(
                    fac.AntdCol(
                        [
                            fac.AntdText(
                                [
                                    '繼續代表您同意愛美膚',
                                    html.A(
                                        '「服務條款」',
                                        href='/terms',
                                    ),
                                    '與',
                                    html.A(
                                        '「隱私權政策」',
                                        href='/privacy-policy',
                                    ),
                                ],
                                type='secondary',
                            ),
                        ],
                    ),
                    justify='center',
                ),
                is_open=is_open,
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
        centered=True,
        renderFooter=False,
    )