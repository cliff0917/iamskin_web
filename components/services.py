import dash_bootstrap_components as dbc

from components import single_service

def serve():
    services = dbc.Row(
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
        style={
            "padding": "2rem 1rem",
        },
    )
    return services