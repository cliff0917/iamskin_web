import dash_uploader as du
from flask import session

def serve(types):
    uploader = du.Upload(
        text='點擊或拖曳圖片',
        text_completed='成功上傳 ',
        cancel_button=True,
        pause_button=True,
        max_file_size=1024,  # 檔案大小限制, 要去 /etc/nginx/nginx.conf 設定
        filetypes=['jpg', 'jpeg', 'png'],
        default_style={
            'background-color': '#fafafa',
            'font-weight': 'bold',
            "margin-top": '2rem',
        },
        id={
            'type': 'upload',
            'index': types
        },
        upload_id=types,
        # upload_id=f'{types}/{session["google_id"]}',
    )
    return uploader