import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import dcc, html

def serve(service_type):
    col_style = {
        'width': 6,
        'margin-top': '2rem',
        'margin-left': '1rem',
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
                                    'index': service_type
                                },
                            ),
                            fac.AntdImage(
                                id={
                                    'type': 'upload-img',
                                    'index': service_type
                                },
                                locale='en-us'
                            ),
                        ],
                        style=col_style,
                    ),
                    dbc.Col(
                        id={
                            'type':'output-info',
                            'index': service_type
                        },
                        style=col_style,
                    ),
                ],
            ),
            html.H2(
                id={
                    'type': 'predict-class',
                    'index': service_type
                },
                style={'font-weight': 'bold', 'margin-top': '2rem'},
            ),
            html.Ul(
                id={
                    'type': 'advice',
                    'index': service_type
                },
            ),
            dbc.Collapse(
                fac.AntdRow(
                    fac.AntdCol(
                        fac.AntdButton(
                            html.P(
                                '分享預測結果至評論區',
                                style={
                                    'font-weight': 'bold',
                                }
                            ),
                            type='primary',
                            size='large',
                            nClicks=0,
                            id={
                                'type': 'share-btn',
                                'index': service_type
                            }
                        ),
                    ),
                    justify='center',
                ),
                is_open=False,
                id={
                    'type': 'share-btn-collapse',
                    'index': service_type
                }
            ),
        ]
    )