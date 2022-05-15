import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback

MAP_LAYOUT = html.Div(
    [
        dcc.Interval(id="map_page_interval", interval=15 * 1000, n_intervals=0),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="map_page_map_1",
                        style={
                            "padding": "10px",
                            "float": "left",
                            "width": "5",
                            "height": "50vh",
                        },
                    ),
                ),
                dbc.Col(
                    dcc.Graph(
                        id="map_page_map_2",
                        style={
                            "padding": "10px",
                            "float": "right",
                            "width": "5",
                            "height": "50vh",
                        },
                    )
                ),
            ]
        ),
    ],
    className="h-50",
)

try:
    print(n)
except:
    print("Starting Generator")
    bpm_by_month_generator = data_con.bpm_by_month_map_data("STARTED")


@callback(
    Output("map_page_map_1", "figure"),
    Output("map_page_map_2", "figure"),
    Input("map_page_interval", "n_intervals"),
)
def get_data_and_visuals(n):

    bpm_by_month_data = next(bpm_by_month_generator)
    mapfig1 = viz.build_map_one(bpm_by_month_data)
    return mapfig1, mapfig1
