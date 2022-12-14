import feffery_antd_components as fac
from dash import html

import globals

def serve():
    login_modal = fac.AntdModal(
        [
            html.A(
                fac.AntdRow(
                    fac.AntdCol(
                        fac.AntdButton(
                            html.Img(
                                src=f"{globals.config['img_path']}/google.png", 
                                height="30px",
                            ),
                            style={
                                'height': '40px',
                            }
                        ),
                    ),
                    justify='center',
                ),
                href='/login',
            )
        ],
        id='modal',
        visible=False,
        title=fac.AntdRow(
            fac.AntdCol(
                fac.AntdTitle(
                    '登入帳號', 
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
    return login_modal