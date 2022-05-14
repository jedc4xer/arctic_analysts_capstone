import data_control as data_con
import visual_control as viz
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
from dash.exceptions import PreventUpdate

# This code structures the layout for this page.

ANALYSIS_LAYOUT = html.Div(
    [
        dcc.Interval(id="analysis_page_interval", interval=30 * 1000, n_intervals=0),
        # dbc.Row(html.H1("US Housing Analysis"), className="text-center"),
        dbc.Row(html.Div(id="analysis_page_record_count"), className="text-center",),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="analysis_page_first",
                        # figure=fig1, For a static graph I believe this is useful
                        style={
                            "padding": "10px",
                            "border-radius": "20px",
                            "float": "left",
                            "width": "2",
                            "height": "50vh",
                        },
                    )
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="analysis_page_second",
                            style={
                                "padding": "10px",
                                "float": "right",
                                "width": "6",
                                "height": "25vh",
                            },
                        ),
                        dcc.Graph(
                            id="analysis_page_third",
                            style={
                                "padding": "10px",
                                "float": "right",
                                "width": "6",
                                "height": "25vh",
                            },
                        ),
                    ]
                ),
            ],
            className="h-75",
        ),
        dbc.Row(
            [
                dcc.Graph(
                    id="analysis_page_fourth",
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
    Output("analysis_page_second", "figure"),
    Output("analysis_page_third", "figure"),
    Output("analysis_page_fourth", "figure"),
    #     Output("record_count", "children"),
    Input("analysis_page_interval", "n_intervals"),
    # prevent_initial_call=True,
)
def get_data_and_visualize(n):
    # Get the Data
    data_dict = get_data()

    # Send the Data to the Visual Builder
    fig1, fig2, fig3, fig4 = analysis_viz_builders(data_dict)

    # fig4 = viz.build_fig_four(data_dict['house_prices'])
    return fig1, fig2, fig3, fig4


def get_data():
    data_dict = data_con.prepare_data()
    return data_dict


def analysis_viz_builders(data_dict):
    # function calls for visualization builders
    # Starter for initial dash populating
    fig1 = viz.build_fig_one()

    fig2 = viz.build_fig_two()

    fig3 = viz.build_fig_three(data_dict["median_income"])

    fig4 = viz.build_fig_four(data_dict["house_prices"])

    # fig4 = viz.build_fig_four()

    return fig1, fig2, fig3, fig4
