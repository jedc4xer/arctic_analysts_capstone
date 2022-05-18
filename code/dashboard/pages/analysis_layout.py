import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
from dash.exceptions import PreventUpdate
import functools

try:
    yearly_income = data_con.income_data_generator()
except Exception as E:
    print("Error", E)
        
@functools.lru_cache()
def analysis_viz_builders():
    # function calls for visualization builders
    # Starter for initial dash populating
    fig1 = viz.build_fig_two()

    fig2 = viz.build_fig_two()

    fig3 = viz.build_fig_two()

    # fig3 = viz.build_fig_three(data_dict["median_income"])

    # fig4 = viz.build_income_line_chart(data_con.income_data())

    fig4 = viz.build_fig_four()

    return fig1, fig2, fig3, fig4


fig1, fig2, fig3, fig4 = analysis_viz_builders()


# This code structures the layout for this page.

ANALYSIS_LAYOUT = html.Div(
    [
        # dcc.Interval(id="analysis_page_interval", interval=5 * 1000, n_intervals=0),
        # dbc.Row(html.H1("US Housing Analysis"), className="text-center"),
        dbc.Row(html.Div(id="analysis_page_record_count"), className="text-center",),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Interval(id="graph_1", interval=.5 * 1000, n_intervals=0),
                        dcc.Graph(
                            id="analysis_page_first",
                            #figure=fig1,
                            style={"padding": "10px", "float": "left", "height": "50vh",},
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="analysis_page_second",
                            figure=fig2,
                            style={
                                "padding": "10px",
                                "float": "right",
                                "height": "25vh",
                            },
                        ),
                        dcc.Graph(
                            id="analysis_page_third",
                            figure=fig3,
                            style={
                                "padding": "10px",
                                "float": "right",
                                "height": "25vh",
                            },
                        ),
                    ],
                    width="3",
                ),
            ],
            className="h-50",
        ),
        dbc.Row(
            [
                dcc.Interval(id="graph_2", interval=.5 * 1000, n_intervals=0),
                dcc.Graph(
                    id="median_income_chart",
                    #figure=fig4,
                    style={
                        "padding": "10px",
                        "float": "right",
                        "width": "12",
                        "height": "40vh",
                    },
                )
            ],
            className="h-25",
        ),
    ]
)

@callback(
    Output("analysis_page_first", "figure"),
    Output("median_income_chart", "figure"),
    Input("graph_1", 'n_intervals')
    )
def analysis_viz_builders1(n):
    fig1 = viz.build_fig_one(yearly_income)
    return fig1, fig1

# @callback(
#     Output("median_income_chart", "figure"),
#     Input("graph_2", 'n_intervals')
#     )
# def analysis_viz_builders1(n):
#     fig1 = viz.build_fig_one(yearly_income)
#     return fig1