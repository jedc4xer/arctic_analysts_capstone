import time
import visual_control as viz
import new_data_control as new_data_con
import dash_bootstrap_components as dbc
from config import base_maps, age_groups
from dash import Input, Output, dcc, html, callback

arima_gen = None
arima_gen = new_data_con.get_model()

master_df = next(arima_gen)

try:
    income_data_for_map = new_data_con.income_data()
    affordability_gen = new_data_con.calculate_affordability(master_df)
    print(next(affordability_gen))
except Exception as E:
    print("Map Layout: Exception 1A", E)

years = [_ for _ in range(2005, 2023)]

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
                        placeholder="Change Mode",
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
                dbc.Col(width=1),
                # dbc.Col([
                #     dcc.Input(id='range', type='number', min=2, max=10, step=1,
                #               style={'background-color': 'lightgrey'},
                #              placeholder = "Downpayment")],
                #     width=1),
                # dbc.Col([
                #     dcc.Input(id='range', type='number', min=15, max=30, step=15,
                #               style={'background-color': 'lightgrey'},
                #              placeholder = "Mortgage Term")],
                #     width=1),
                # dbc.Col([
                #     dcc.Input(id='range', type='number', min=2, max=10, step=1,
                #               style={'background-color': 'lightgrey'},
                #              placeholder = "Tax Rate")],
                #     width=1),
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
                            "height": "75vh",
                            "margin-top": "10px",
                            "box-shadow": "1px 2px 4px 7px lightgrey",
                        },
                        config={"displayModeBar": False},
                    ),
                ),
                dbc.Col(
                    dcc.Graph(
                        id="map2",
                        # figure=mapfig2,
                        style={
                            "padding": "2px",
                            "float": "left",
                            "width": "2",
                            "height": "75vh",
                            "margin-top": "10px",
                            "box-shadow": "1px 2px 4px 7px lightgrey",
                        },
                        config={"displayModeBar": False},
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
        base_map_style = "stamen-watercolor"

    if age_group is None:
        age_group = "25-44"
    
    if animate is None:
        animate = "static"
        
    if year is None:
        year = 2019
        
    elif year > 2019:
        args = [0.12, 0.25, 30, 0.0189, "annual"]
        animate = 'static_table'
        time.sleep(.5)
        try:
            table = viz.map_builder(
                affordability_gen, base_map_style, age_group, year, animate, args
            )
        except:
            return viz.blank()
        
        return table
    args = False
    
    map1 = viz.map_builder(
        income_data_for_map, base_map_style, age_group, year, animate, args
    )
  
    return map1


@callback(
    Output("map2", "figure"),
    Input("base_map_style", "value"),
    Input("age_dropdown", "value"),
    Input("year_dropdown", "value"),
    Input("animation_dropdown", "value"),
)
def modify_map2(base_map_style, age_group, year, animate):
    if base_map_style is None:
        base_map_style = "stamen-watercolor"

    if age_group is None:
        age_group = "25-44"

    animate = "static-affordability"
    

    if year is None:
        year = 2021
    # year = 2010

    args = [0.12, 0.25, 30, 0.0189, "annual"]
    
    try:
        map2 = viz.map_builder(
            affordability_gen, base_map_style, age_group, year, animate, args
        )
    except Exception as E:
        print(E)
        return viz.blank()
    return map2
