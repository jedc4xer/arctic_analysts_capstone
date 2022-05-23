# import data_control as data_con
import visual_control as viz
from config import locale_options, shadow
import dash_bootstrap_components as dbc
import new_data_control as new_data_con
from dash.exceptions import PreventUpdate
from dash import Input, Output, dcc, html, callback
import time


try:
    yearly_income = new_data_con.income_data_generator()
    home_prices = new_data_con.home_price_data_generator()
except Exception as E:
    print("Analysis Layout: Exception 1A", E)


def analysis_viz_builders():
    # Any static graphs that need to be build on first load.
    return charts


# charts = analysis_viz_builders()


# LAYOUT
########################################

# This code structures the layout for this page.
ANALYSIS_LAYOUT = html.Div(
    [
        # dcc.Interval(id="analysis_page_interval", interval=5 * 1000, n_intervals=0),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="locale_dropdown",
                        options=[
                            {"label": locale_options[i], "value": i}
                            for i in locale_options
                        ],
                        placeholder="Choose a Location",
                        style={
                            "margin-right": "12em",
                            "color": "black",
                            "border": "1px solidgrey",
                        },
                    ),
                ),
                dbc.Col(),
                dbc.Col(),
                dbc.Col(),
            ]
        ),
        dbc.Row(html.Div(id="analysis_page_record_count"), className="text-center",),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id="analysis_page_first",
                            style={
                                "padding": "0px",
                                "float": "left",
                                "height": "40vh",
                                "margin-top": "10px",
                                "box-shadow": shadow,  # Set on config page
                            },
                            config={"displayModeBar": False},
                        ),
                    ]
                ),
                dcc.Interval(id="graph_1", interval=1 * 1000, n_intervals=0),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="home_price_chart",
                            # figure=fig2,
                            style={
                                "padding": "0px",
                                "float": "right",
                                "height": "40vh",
                                "margin-top": "10px",
                                "box-shadow": shadow,  # Set on config page
                            },
                            config={"displayModeBar": False},
                        ),
                    ],
                    width="4",
                ),
            ],
            className="h-50",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id="median_income_chart",
                            # figure=fig4,
                            style={
                                "padding": "0px",
                                "float": "left",
                                "height": "35vh",
                                "margin-top": "15px",
                                "border-color": "black",
                                "box-shadow": shadow,  # Set on config page
                            },
                            config={"displayModeBar": False},
                        ),
                    ],
                    width="2",
                ),
            ],
            className="h-25",
        ),
    ]
)


@callback(
    # Output("analysis_page_first", "figure"),
    # Output("median_income_chart", "figure"),
    Output("home_price_chart", "figure"),
    Input("graph_1", "n_intervals"),
    Input("locale_dropdown", "value"),
    prevent_initial_call=True
)
def analysis_viz_builders(n, locale_value):

    if locale_value is None:
        locale_value = "34001"

    try:
        # fig1, fig2 = viz.income_visual_master(yearly_income, locale_value)
        fig3 = viz.home_price_visual_master(home_prices, locale_value)
    except Exception as E:
        return viz.blank()

    return fig3


@callback(
    Output("analysis_page_first", "figure"),
    Output("median_income_chart", "figure"),
    Input("locale_dropdown", "value"),
)
def update_visual_one(locale):
    locale = "34001" if locale is None else locale

    time.sleep(1)
    fig, fig1 = viz.income_visual_master(yearly_income, locale)
    return fig, fig1


# @callback(
#     Output("median_income_chart", "figure"),
#     Input("graph_2", 'n_intervals')
#     )
# def analysis_viz_builders1(n):
#     fig1 = viz.build_fig_one(yearly_income)
#     return fig1
