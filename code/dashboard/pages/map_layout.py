import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import functools
from config import base_maps, age_groups


# @functools.lru_cache()
# def get_data_and_visuals():

#     mapfig1 = viz.build_static_map_one()
#     mapfig2 = viz.build_static_map_two()
#     return mapfig1, mapfig2


# mapfig1, mapfig2 = get_data_and_visuals()

MAP_LAYOUT = html.Div(
    [
        # Not sure that we really want an interval on this page
        # dcc.Interval(id="map_page_interval", interval=15 * 1000, n_intervals=0),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='base_map_style',
                         options = [
                             {"label": base_maps[i], "value": i}
                             for i in base_maps
                         ],
                        placeholder="Change the Map Style",
                        style={
                            "color": "black"
                        }
                    ),width=2,
                ),
                
                dbc.Col(
                    dcc.Dropdown(
                        id='animation_dropdown',
                         options = [
                             {"label": 'Static Map', "value": 'static'},
                             {"label": 'Animated Map', 'value': 'animated'}
                         ],
                        placeholder="Modify Map",
                        style={
                            "color": "black"
                        }
                    ),width=2,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='age_dropdown',
                         options = [
                             {"label": age_groups[i], "value": i}
                             for i in age_groups
                         ],
                        placeholder="Age",
                        style={
                            "color": "black"
                        }
                    ),width=1,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='year_dropdown',
                         options = [
                             {"label": 'Not Implemented', "value": 'None'}
                         ],
                        placeholder="Year",
                        style={
                            "color": "black"
                        }
                    ),width=1,
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
                        #figure=map1,
                        style={
                            "padding": "2px",
                            "float": "left",
                            "width": "2",
                            "height": "80vh",
                        },
                    ),
                ),
                dbc.Col(
                    dcc.Graph(
                        id="map_page_map_2",
                        #figure=mapfig2,
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
    Input("base_map_style", 'value'),
    Input("age_dropdown", 'value'),
    Input("animation_dropdown", 'value')
)
def modify_map(base_map_style, age_group, animate):
    if base_map_style is None:
        base_map_style = "open-street-map"
        
    if age_group is None:
        age_group = '25-44'
        
    if animate is None:
        animate = 'static'
    
    
    map1 = viz.map_builder(base_map_style, age_group, animate)
    return map1

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
