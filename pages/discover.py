import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ALL

from process_time import process_time
from components import fields, datePicker, discover_display, collapse_item

# components
hitNum = html.H1(
    [
        '載入資料中',
        dbc.Spinner(size="lg", spinner_style={'margin-left': '15px', 'width': '40px', 'height': '40px'}),
    ],
    style={'textAlign': 'center'}, id='dataNum'
)

DISPLAY_STYLE = {
    "transition": "margin-left .5s",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    # 'border':'1px black solid',
    'width': '1px',
    'zIndex':1,
}

def serve_layout():
    layout = html.Div(
        [
            dbc.Row(
                [
                    fields.serve_fields(),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    datePicker.discover_date_picker(),   # live update
                                ]
                            ),
                            dcc.Loading(
                                html.Div(
                                    [
                                        hitNum,
                                        dbc.Col(id='graph-and-table'),
                                    ],
                                ),
                            ),
                        ],
                        style=DISPLAY_STYLE,
                    ),
                ],
            ),
        ],
    )
    return layout

# 初始化 display or 按下 Update 按鈕的觸發事件 or 利用 fields_btn 來動態 update display
@callback(
    [
        Output('datetime-output', 'children'),
        Output('dataNum', 'children'),
        Output("graph-and-table", "children"),
    ],
    [
        Input('submit_date', 'n_clicks'),
        Input({'type': 'add_btn', 'index': ALL}, 'n_clicks'),
        Input({'type': 'del_btn', 'index': ALL}, 'n_clicks'),
    ],
    [
        State('datetime-picker', 'value')
    ]
)
def update(n_clicks, add_btn, del_btns, time):
    # 將 time 轉成 timestamp format, 並得到 interval
    startDate, endDate, freqs = process_time.get_time_info(time)
    return discover_display.update(startDate, endDate, freqs)