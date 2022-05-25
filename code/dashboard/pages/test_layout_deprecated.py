# import data_control as data_con
# import visual_control as viz
# import dash_bootstrap_components as dbc
# from dash import Input, Output, dcc, html, callback


# def get_data_and_visuals():

#     mapfig1 = viz.build_static_map_one()
#     return mapfig1


# TEST_LAYOUT = html.Div(
#     [
#         dbc.Row(html.H1("Test Page"), className="text-center"),
#         dbc.Row(
#             [
#                 dbc.Col(
#                     dcc.Graph(
#                         id="test_page_map_1",
#                         # figure = fig1,
#                         style={
#                             "padding": "5px",
#                             "float": "left",
#                             "width": "4",
#                             "height": "75vh",
#                         },
#                     ),
#                 ),
#                 dbc.Col(
#                     dcc.Graph(
#                         id="test_page_map_2",
#                         # figure = fig2,
#                         style={
#                             "padding": "10px",
#                             "float": "right",
#                             "width": "5",
#                             "height": "75vh",
#                         },
#                     )
#                 ),
#             ]
#         ),
#     ],
#     className="h-100",
# )
