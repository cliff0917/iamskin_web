from dash import html

import globals
from components import card, upload

def serve_layout(types, tutorial_isOpen):
    layout = html.Div(
        [
            card.serve(
                globals.config["service_intro"][types]["title"],
                globals.config["service_intro"][types]["content"],
                tutorial_isOpen,
                types,
            ),
            upload.serve(),
        ],
    )
    return layout