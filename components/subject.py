import feffery_antd_components as fac

import globals

def serve():
    with open(f"{globals.config['text_path']}/subject.txt", 'r') as f:
        content = f.read()

    subject = fac.AntdCard(
        fac.AntdParagraph(
            content,
        ),
        title='主旨',
        headStyle={
            'fontSize': 35,
            'font-weight': 'bold',
        },
        hoverable=True,
        bodyStyle={
            'fontSize': 30,
        },
        style={
            "margin-top": "2rem",
        },
    )
    return subject