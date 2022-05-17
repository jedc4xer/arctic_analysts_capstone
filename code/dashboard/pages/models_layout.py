import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback


MODEL_LAYOUT = html.Div(
    [
        dbc.Row(html.H1("Machine Learning Models Page"), className="text-center"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="model_img_1",
                        style={
                            "padding": "5px",
                            "float": "left",
                            "width": "4",
                            "height": "75vh",
                        },
                    ),
                ),
                dbc.Col(
                    dcc.Graph(
                        id="model_img_2",
                        style={
                            "padding": "10px",
                            "float": "right",
                            "width": "5",
                            "height": "75vh",
                        },
                    )
                ),
            ]
        ),
    ],
    className="h-100",
)
