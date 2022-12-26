import feffery_antd_components as fac
from flask import session

def serve(path, width):
    return fac.AntdImage(
        src=path,
        locale='en-us',
        style={
            'width': width,
            'padding': '1rem 1rem',
        }
    )