import feffery_antd_components as fac

def serve():
    upload = fac.AntdPictureUpload(
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
            'margin-top': '1rem',
        },
        locale='en-us',
    )
    return upload