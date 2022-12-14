import feffery_antd_components as fac

def serve():
    login_btn = fac.AntdButton(
        '登入',
        type='primary',
        style={
            "font-weight": "bold",
        },
        size='large',
        id='login-btn',
    )
    return login_btn