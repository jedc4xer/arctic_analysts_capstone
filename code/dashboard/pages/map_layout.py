import new_data_control as new_data_con
import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import functools
from config import base_maps, age_groups

try:
    income_data_for_map = new_data_con.income_data()
except Exception as E:
    print("Map Layout: Exception 1A", E)
    
years = [_ for _ in range(2005, 2020)]

MAP_LAYOUT = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="base_map_style",
                        options=[
                            {"label": base_maps[i], "value": i} for i in base_maps
                        ],
                        placeholder="Change the Map Style",
                        style={"color": "black"},
                    ),
                    width=2,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="animation_dropdown",
                        options=[
                            {"label": "Static Map", "value": "static"},
                            {"label": "Animated Map", "value": "animated"},
                        ],
                        placeholder="Modify Map",
                        style={"color": "black"},
                    ),
                    width=2,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="age_dropdown",
                        options=[
                            {"label": age_groups[i], "value": i} for i in age_groups
                        ],
                        placeholder="Age",
                        style={"color": "black"},
                    ),
                    width=1,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="year_dropdown",
                        options=[{"label": y, "value": y} for y in years],
                        placeholder="Year",
                        style={"color": "black"},
                    ),
                    width=1,
                ),
                dbc.Col(width=4),
                dbc.Col(width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="map1",
                        # figure=map1,
                        style={
                            "padding": "2px",
                            "float": "left",
                            "width": "2",
                            "height": "80vh",
                        },
                        config={"displayModeBar": False},
                    ),
                ),
                dbc.Col(
                    dcc.Graph(
                        id="map_page_map_2",
                        # figure=mapfig2,
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


@callback(
    Output("map1", "figure"),
    Input("base_map_style", "value"),
    Input("age_dropdown", "value"),
    Input("year_dropdown", "value"),
    Input("animation_dropdown", "value"),
)
def modify_map(base_map_style, age_group, year, animate):
    if base_map_style is None:
        base_map_style = "open-street-map"

    if age_group is None:
        age_group = "25-44"

    if animate is None:
        animate = "static"
        
    if year is None:
        year = 2019

    map1 = viz.map_builder(income_data_for_map, base_map_style, age_group, year, animate)
    return map1