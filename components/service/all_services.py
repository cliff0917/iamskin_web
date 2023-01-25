import dash_bootstrap_components as dbc
from dash import html

from components.service import single_service

def serve():
    services = html.Div(
        [
            single_service.serve(
                '膚質',
                'Skin',
                False,
            ),
            single_service.serve(
                '指甲',
                'Nail',
                False,
            ),
            single_service.serve(
                '痘痘',
                'Acne',
                True,
            ),
        ],
    )
    return services