import feffery_antd_components as fac
from flask import session

def serve():
    # 如果 session 中沒有 google_id, 則 navbar 右上角顯示登入
    if session.get('google_id', None) == None:
        return fac.AntdButton(
            '登入',
            type='primary',
            style={
                "font-weight": "bold",
            },
            size='large',
            id='login-btn',
        )
    
    # 如果 session 中存在 google_id, 則 navbar 右上角顯示使用者的照片
    else:
        return fac.AntdButton(
            fac.AntdAvatar(
                mode='image',
                src=session["picture"],
                size=48,
                style={
                    'margin-bottom': '10px',
                },
            ),
            type='link',
            style={
                'margin-bottom': '1.5rem',
            },
            nClicks=0,
            id='avatar',
        )