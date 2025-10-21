from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.CERULEAN,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

server = app.server