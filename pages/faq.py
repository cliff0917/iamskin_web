import feffery_antd_components as fac
from dash import html

def serve_layout():
    layout = html.Div(
        [
            fac.AntdTitle('常見問題', level=1),
            html.Hr(),
            fac.AntdCollapse(
                [
                    fac.AntdParagraph('我們提供三項功能'),
                    html.Ul(
                        [
                            html.Li('膚質檢測 (檢測您的膚質為乾性肌、油性肌、敏感肌)'),
                            html.Li('指甲檢測 (檢測您的指甲異常風險)'),
                            html.Li('痘痘檢測 (檢測您痘痘的嚴重程度)'),
                        ]
                    ),
                    fac.AntdText(
                        '※ 注意事項：此服務僅作為風險之初步判斷，以達到適時預防之功能。如需更詳細的檢查，請務必尋求專業醫療單位。',
                        type="danger",
                    ),
                ],
                title='愛美膚有什麼功能？',
                is_open=False,
            ),
            fac.AntdCollapse(
                fac.AntdText('不需要！這些服務完全免費！'),
                title='使用檢測服務需要收費嗎？',
                is_open=False,
                style={
                    'margin-top': '1rem',
                },
            ),
            fac.AntdCollapse(
                fac.AntdText('不會的！圖片經由 AI 判讀後會立即刪除，不會做任何的存檔，請您放心。'),
                title='使用服務時上傳的圖片會不會有資安疑慮？',
                is_open=False,
                style={
                    'margin-top': '1rem',
                },
            ),
        ]
    )
    return layout