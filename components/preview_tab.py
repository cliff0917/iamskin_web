from dash import html
import dash_bootstrap_components as dbc
import feffery_antd_components as fac

import globals
from components import bold_text

def serve(types):
    return fac.AntdTabPane(
        html.Div(
            [
                fac.AntdAvatar(
                    mode='icon',
                    size='xs',
                    style={
                        'backgroundColor': 'rgb(16, 105, 246)'
                    }
                ),
                fac.AntdText(
                    f'123',
                    style={
                        'margin-left': '5px',
                    }
                ),
                fac.AntdText(
                    globals.now(),
                    type='secondary',
                    style={
                        'margin-left': '1rem',
                    },
                    id={
                        'type': 'preview-time',
                        'index': types
                    }
                ),
                html.Br(),
                fac.AntdText(
                    f'檢測類別：{globals.config["service_intro"][types]["title"][:2]}',
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
                    defaultValue=3,
                    disabled=True,
                    id={
                        'type': 'preview-rate',
                        'index': types
                    }
                ),
                html.Br(),
                html.Div(
                    [
                        fac.AntdText(
                            style={
                                'font-weight': 'bold',
                            },
                            id={
                                'type': 'preview-comment-title',
                                'index': types
                            }
                        ),
                        fac.AntdText(
                            id={
                                'type': 'preview-comment',
                                'index': types
                            }
                        )
                    ],
                    style={
                        'margin-top': '5px',
                        'margin-left': '1rem',
                    }
                ),
                dbc.Collapse(
                    id={
                        'type': 'preview-img-collapse',
                        'index': types
                    },
                    is_open=True,
                )
            ],
            style={
                'backgroundColor': 'rgba(241, 241, 241, 0.4)',
            }
        ),
        tab='預覽',
        key='預覽'
    )