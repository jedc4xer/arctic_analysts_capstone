import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
from dash.exceptions import PreventUpdate
from config import feature_options, locale_options

start_interval = 5 * 1000
poly_gen = None
poly_gen = data_con.poly_generator()

MODEL_LAYOUT = html.Div(
    [
        # dbc.Row(html.H1("Machine Learning Models Page"), className="text-center"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="feature_dropdown",
                        options=[
                            {"label": feature_options[i], "value": i}
                            for i in feature_options
                        ],
                        placeholder="Select a Feature",
                        style={
                            "margin-right": "12em",
                            "color": "black",
                            "border": "1px solidgrey",
                        },
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="locale_dropdown",
                        options=[
                            {"label": locale_options[i], "value": i}
                            for i in locale_options
                        ],
                        placeholder="Select a Locale",
                        style={
                            "margin-right": "4em",
                            "color": "black",
                            "border": "1px solidgrey",
                        },
                    )
                ),
                dbc.Col(),
                dbc.Col(),
            ]
        ),
        dcc.Interval(id="model_intervals", interval=start_interval, n_intervals=0),
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
    Output("model_intervals", "interval"),
    Input("model_intervals", "n_intervals"),
    Input("feature_dropdown", "value"),
    Input("locale_dropdown", "value"),
    Input("model_intervals", "interval"),
)
def model_builders(n, feature_value, locale_value, interval):
    if feature_value is None:
        feature_value = "MedianHousePrice"

    if locale_value is None:
        locale_value = "34001"
    try:
        data, best = next(poly_gen)
    except Exception as E:
        if E == "generator already executing":
            print("Caught: Generator is already executing.")
        else:
            print(E)

    if data is None:
        return html.H2("Waiting for the data. ")

    poly_gen.send([feature_value, locale_value])

    fig1 = viz.build_polynomial_model(data, feature_value, locale_value, best)
    if best:
        new_interval = 10 * 1000
        return fig1, fig1, new_interval
    else:
        new_interval = 0.2 * 1000
        return fig1, fig1, new_interval
