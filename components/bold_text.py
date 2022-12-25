import feffery_antd_components as fac

def serve(text):
    return fac.AntdText(
        text,
        style={
            'font-weight': 'bold',
        },
    )