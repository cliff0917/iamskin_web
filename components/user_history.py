from dash import html
import feffery_antd_components as fac
from flask import session

import globals, database

def serve():
    history = database.get_history(session["google_id"])

    return html.Div(
        [
            
            fac.AntdTable(
                columns=[
                    {
                        'title': '編號',
                        'dataIndex': '編號'
                    },
                    {
                        'title': '檢測類別',
                        'dataIndex': '檢測類別'
                    },
                    {
                        'title': '上傳時間',
                        'dataIndex': '上傳時間'
                    },
                    {
                        'title': '上傳圖片',
                        'dataIndex': '上傳圖片',
                        'renderOptions': {
                            'renderType': 'image'
                        }
                    },
                    {
                        'title': '輸出',
                        'dataIndex': '輸出',
                        'renderOptions': {
                            'renderType': 'image'
                        }
                    }
                ],
                data=[
                    {
                        '編號': i + 1,
                        '檢測類別': globals.config["chinese"][types]["normal"],
                        '上傳時間': upload_time,
                        '上傳圖片': {
                            'src': f'assets/upload/{types}/{session["google_id"]}/{upload_time}/{file_name}',
                            'height': '75px'
                        },
                        '輸出': {
                            'src': f'assets/prediction/{types}/{session["google_id"]}/{upload_time}/{file_name}',
                            'height': '75px'
                        }
                    }
                    for i, [types, upload_time, file_name] in enumerate(history)
                ],
                bordered=True,
                locale='en-us',
                pagination={
                    'pageSize': 5,
                    'current': 1,
                    'showTotalPrefix': '總共 ',
                    'showTotalSuffix': '筆資料'
                },
                sortOptions={
                    'sortDataIndexes': ['編號']
                },
                filterOptions={
                    '檢測類別': {
                        'filterMode': 'checkbox',
                        'filterCustomItems': [chinese["normal"] for _, chinese in globals.config["chinese"].items()]
                    }
                }
            )
        ]
    )