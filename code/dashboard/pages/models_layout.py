import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback


# try:
#     data_hold = data_con.get_and_hold_data()
# except:
#     print('DataHold is already activated.')
poly_gen = None
try:
    poly_gen = data_con.poly_generator()
except:
    print('Model is already run')
    
    
MODEL_LAYOUT = html.Div(
    [
        dbc.Row(html.H1("Machine Learning Models Page"), className="text-center"),
        dcc.Interval(id="model_intervals", interval= .2 * 1000, n_intervals=0),
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

@callback(
    Output("model_img_1", "figure"),
    Output("model_img_2", "figure"),
    Input("model_intervals", 'n_intervals')
    )
def analysis_viz_builders1(n):
    #data = next(data_hold)
    data = next(poly_gen)
    fig1 = viz.build_polynomial_model(data)
    return fig1, fig1
