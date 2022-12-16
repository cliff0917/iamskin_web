import feffery_antd_components as fac

def serve(session):
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