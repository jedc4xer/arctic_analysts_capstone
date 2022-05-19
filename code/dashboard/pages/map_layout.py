import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import functools


@functools.lru_cache()
def get_data_and_visuals():

    mapfig1 = viz.build_static_map_one()
    mapfig2 = viz.build_static_map_two()
    return mapfig1, mapfig2


mapfig1, mapfig2 = get_data_and_visuals()

MAP_LAYOUT = html.Div(
    [
        # Not sure that we really want an interval on this page
        # dcc.Interval(id="map_page_interval", interval=15 * 1000, n_intervals=0),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="map_page_map_1",
                        figure=mapfig1,
                        style={
                            "padding": "5px",
                            "float": "left",
                            "width": "5",
                            "height": "80vh",
                        },
                    ),
                ),
                dbc.Col(
                    dcc.Graph(
                        id="map_page_map_2",
                        figure=mapfig2,
                        style={
                            "padding": "5px",
                            "float": "right",
                            "width": "5",
                            "height": "80vh",
                        },
                    )
                ),
            ]
        ),
    ],
    className="h-50",
)

# try:
#     print(n)
# except:
#     print("Starting Generator")
#     bpm_by_month_generator = data_con.bpm_by_month_map_data("STARTED")


# @callback(
#     Output("map_page_map_1", "figure"),
#     Output("map_page_map_2", "figure"),
#     Input("map_page_interval", "n_intervals"),
# )
# def get_data_and_visuals(n):

#     mapfig1 = viz.build_static_map_one()
#     mapfig2 = viz.build_static_map_two()
#     return mapfig1, mapfig1

# def get_data_and_visuals():

#     mapfig1 = viz.build_static_map_one()
#     mapfig2 = viz.build_static_map_two()
#     return mapfig1, mapfig2


# mapfig1, mapfig2 = get_data_and_visuals()
