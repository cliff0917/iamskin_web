import feffery_antd_components as fac
from dash import html

def serve():
    sidebar = html.Div(
        [
            fac.AntdLayout(
                [
                    fac.AntdAffix(
                        fac.AntdSider(
                            [
                                html.Div(
                                    [
                                        fac.AntdMenu(
                                            menuItems=[
                                                {
                                                    'component': 'Item',
                                                    'props': {
                                                        'key':  '/Home',
                                                        'title': '首頁',
                                                        'icon': 'antd-home',
                                                        'href': '/Home',
                                                    },
                                                },
                                                {
                                                    'component': 'Item',
                                                    'props': {
                                                        'key':  '/About-us',
                                                        'title': '關於我們',
                                                        'icon': 'antd-global',
                                                        'href': '/About-us',
                                                    },
                                                },
                                                {
                                                    'component': 'SubMenu',
                                                    'props': {
                                                        'key':  'AI-Prediction',
                                                        'title': '服務項目',
                                                        'icon': 'antd-bar-chart',
                                                    },
                                                    'children': [
                                                        {
                                                            'component': 'Item',
                                                            'props': {
                                                                'key': '/Skin',
                                                                'title': '膚質檢測',
                                                                'href': '/Skin',
                                                                'icon': 'antd-camera',
                                                            }
                                                        },
                                                        {
                                                            'component': 'Item',
                                                            'props': {
                                                                'key': '/Nail',
                                                                'title': '指甲檢測',
                                                                'href': '/Nail',
                                                                'icon': 'antd-alert',
                                                            }
                                                        },
                                                        {
                                                            'component': 'Item',
                                                            'props': {
                                                                'key': '/Acne',
                                                                'title': '痘痘檢測',
                                                                'href': '/Acne',
                                                                'icon': 'antd-aim',
                                                            }
                                                        }
                                                    ],
                                                },
                                                {
                                                    'component': 'Item',
                                                    'props': {
                                                        'key':  '/Discuss',
                                                        'title': '討論區',
                                                        'icon': 'antd-comment',
                                                        'href': '/Discuss',
                                                    },
                                                },
                                            ],
                                            mode='inline',
                                            defaultOpenKeys=['AI-Prediction'], # 自動展開
                                        )
                                    ],
                                    style={
                                        'height': '100%',
                                        'overflowY': 'auto',
                                    }
                                ),
                            ],
                            id='sider',
                            collapsible=True,
                            style={
                                'backgroundColor': 'rgb(240, 242, 245)',
                            },
                        ),
                        offsetTop=80,
                    ),

                    fac.AntdContent(
                        html.Div(
                            children=[]
                        ),
                        id='content',
                        style={
                            'backgroundColor': '#F7F7F8',
                            'padding': '2rem 1rem',
                            'height': '700vh',
                        }
                    ),
                ],
            )
        ],
    )
    return sidebar