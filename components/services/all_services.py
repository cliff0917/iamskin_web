import dash_bootstrap_components as dbc
from dash import html

from components.services import single_service

def serve():
    services = html.Div(
        dbc.Row(
            [
                single_service.serve(
                    '膚質',
                    'Skin',
                ),
                single_service.serve(
                    '指甲',
                    'Nail',
                ),
                single_service.serve(
                    '痘痘',
                    'Acne',
                ),
            ],
        )
    )
    return services