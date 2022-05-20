import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
from dash.exceptions import PreventUpdate
import functools
from config import locale_options

try:
    yearly_income = data_con.income_data_generator()
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
                        dcc.Interval(id="graph_1", interval=0.5 * 1000, n_intervals=0),
                        dcc.Graph(
                            id="analysis_page_first",
                            # figure=fig1,
                            style={
                                "padding": "10px",
                                "float": "left",
                                "height": "45vh",
                            },
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="analysis_page_second",
                            # figure=fig2,
                            style={
                                "padding": "10px",
                                "float": "right",
                                "height": "45vh",
                            },
                        ),
                        # dcc.Graph(
                        #     id="analysis_page_third",
                        #     # figure=fig3,
                        #     style={
                        #         "padding": "10px",
                        #         "float": "right",
                        #         "height": "20vh",
                        #     },
                        # ),
                    ],
                    width="4",
                ),
            ],
            className="h-50",
        ),
        dbc.Row(
            [
                dcc.Interval(id="graph_2", interval=5 * 1000, n_intervals=0),
                dcc.Graph(
                    id="median_income_chart",
                    # figure=fig4,
                    style={
                        "padding": "10px",
                        "float": "right",
                        "width": "12",
                        "height": "40vh",
                    },
                ),
            ],
            className="h-25",
        ),
    ]
)


@callback(
    Output("analysis_page_first", "figure"),
    Output("median_income_chart", "figure"),
    Input("graph_1", "n_intervals"),
    Input("locale_dropdown", "value"),
)
def analysis_viz_builders(n, locale_value):
    if locale_value is None:
        locale_value = "34001"

    try:
        fig1, fig2 = viz.income_visual_master(yearly_income, locale_value)
    except Exception as E:
        print(E)

    return fig1, fig2


# @callback(
#     Output("median_income_chart", "figure"),
#     Input("graph_2", 'n_intervals')
#     )
# def analysis_viz_builders1(n):
#     fig1 = viz.build_fig_one(yearly_income)
#     return fig1
