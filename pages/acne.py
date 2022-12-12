import feffery_antd_components as fac
from dash import html

def serve_layout():
    layout = html.Div(
        [
            fac.AntdCard(
                fac.AntdParagraph(
                    '透過影像分析來檢測您痘痘的嚴重程度。',
                ),
                title='痘痘檢測工具',
                headStyle={
                    'fontSize': 35,
                    'font-weight': 'bold',
                },
                hoverable=True,
                bodyStyle={
                    'fontSize': 30,
                },
            ),
            fac.AntdPictureUpload(
                apiUrl='/upload/',
                fileMaxSize=1,
                buttonContent='點擊上傳圖片',
                failedTooltipInfo='上傳失敗',
                editable=True,
                editConfig={
                    'grid': True,
                    'rotate': True,
                    'modalTitle': '圖片編輯窗口',
                    'modalWidth': 600
                },
                style={
                    'margin-top': '2rem',
                },
                locale='en-us',
            )
        ],
    )
    return layout