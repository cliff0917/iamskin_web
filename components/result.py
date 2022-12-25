import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import dcc, html

def serve(types):
    col_style = {
        'width': 6,
        'margin-top': '2rem',
        'margin-left': '1rem',
        # 'border': '1px black solid',
    }
    return dcc.Loading(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3(
                                style={
                                    'font-weight': 'bold'
                                },
                                id={
                                    'type': 'upload-text',
                                    'index': types
                                },
                            ),
                            html.Img(
                                id={
                                    'type': 'upload-img',
                                    'index': types
                                },
                                style={
                                    'width': '60%'
                                }
                            ),
                        ],
                        style=col_style,
                    ),
                    dbc.Col(
                        id={
                            'type':'output-info',
                            'index': types
                        },
                        style=col_style,
                    ),
                ],
            ),
            dbc.Collapse(
                html.Hr(),
                is_open=False,
                id={
                    'type': 'horizon-line',
                    'index': types
                }
            ),
            html.H2(
                id={
                    'type': 'predict-class',
                    'index': types
                },
                style={'font-weight': 'bold'},
            ),
            html.Ul(
                id={
                    'type': 'advice',
                    'index': types
                },
            ),
            dbc.Collapse(
                fac.AntdRow(
                    fac.AntdCol(
                        fac.AntdButton(
                            html.P(
                                '分享預測結果至討論區',
                                style={
                                    'font-weight': 'bold',
                                }
                            ),
                            type='primary',
                            size='large',
                            nClicks=0,
                            id={
                                'type': 'share-btn',
                                'index': types
                            }
                        ),
                    ),
                    justify='center',
                ),
                is_open=False,
                id={
                    'type': 'share-btn-collapse',
                    'index': types
                }
            ),
        ]
    )