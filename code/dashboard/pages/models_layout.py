import time
import arima_model as arima
import visual_control as viz
import dash_bootstrap_components as dbc
import new_data_control as new_data_con
from dash.exceptions import PreventUpdate
from dash import Input, Output, dcc, html, callback, State
from config import feature_options, locale_options, age_groups, shadow


start_interval = 5 * 1000

# This starts the generator which returns model results for the
# polynomial visualizations. The generator is located in data_control.py
arima_gen = None
arima_gen = new_data_con.get_model()

master_df = next(arima_gen)
adf_gen = new_data_con.run_arima(master_df)
next(adf_gen)


feature_options = {
    "MedianIncome": "Median Income",
    "other": "Median House Price (Gold Tier)",
    "other1": "Average Mortgage Rate (Gold Tier)",
    "other2": "New Buildings (Gold Tier)",
    "other3": "New Units (Gold Tier)",
}

MODEL_LAYOUT = html.Div(
    [
        # dbc.Row(html.H1("Machine Learning Models Page"), className="text-center"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="feature_dropdown",
                        options=[
                            {
                                "label": feature_options[i],
                                "value": i,
                                "disabled": True if "other" in i else False,
                            }
                            for i in feature_options
                        ],
                        placeholder="Select a Feature",
                        style={
                            ##"margin-right": "12em",
                            "color": "black",
                            ##"border": "1px solidgrey",
                        },
                    ),
                    width=3,
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
                            # "margin-right": "4em",
                            "color": "black",
                            # "border": "1px solidgrey",
                        },
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
                dbc.Col(width=3),
            ]
        ),
        dcc.Interval(id="model_intervals", interval=start_interval, n_intervals=0),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="model_img_1",
                        style={
                            "padding": "0px",
                            "float": "left",
                            "width": "4",
                            "height": "75vh",
                            "margin-top": "10px",
                            "box-shadow": "1px 2px 4px 7px lightgrey",
                        },
                        config={"displayModeBar": False},
                    ),
                ),
                dbc.Col(
                    # html.H2(" No visual yet. ")
                    dcc.Graph(
                        id="model_img_2",
                        style={
                            "padding": "0px",
                            "float": "right",
                            "width": "5",
                            "height": "50vh",
                            "margin-top": "10px",
                            "box-shadow": "1px 2px 4px 7px lightgrey",
                        },
                        config={"displayModeBar": False},
                    )
                ),
            ]
        ),
    ],
    className="h-100",
)

# This is the callback function for the visuals on the model page.
@callback(
    Output("model_img_1", "figure"),
    Output("model_img_2", "figure"),
    Output("model_intervals", "interval"),
    Input("model_intervals", "n_intervals"),
    Input("feature_dropdown", "value"),
    Input("locale_dropdown", "value"),
    Input("age_dropdown", "value"),
    Input("model_intervals", "interval"),
)
def model_builder(n, feature_value, locale_value, age_group, interval):
    feature_value = "MedianIncome" if feature_value is None else feature_value
    locale_value = "34001" if locale_value is None else locale_value
    age_group = "25-44" if age_group is None else age_group

    params = [locale_value, age_group]

    best = False
    if best:
        new_interval = 5 * 1000
    else:
        new_interval = 5 * 1000

    try:
        differenced, results = adf_gen.send([feature_value, params])
    except Exception as E:
        print('Differenced Data Generator Failure', E)
        
    try:
        df = arima_gen.send([feature_value, params])
    except Exception as E:
        print('Arima Generator Failure', E)
        
    try:
        fig1, fig2 = viz.arima_visual_controller(
            df, feature_value, params, differenced, results
        )
    except Exception as E:
        print('Model Visual Creation Failure', E)
        return viz.blank(), viz.blank()

    return fig1, fig2, new_interval
