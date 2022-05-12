import dash
from dash import dcc, html
import data_control as data_con
import visualization_builder as viz
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

other_themes = [
    'Cerulean',
    'Cosmo',
    'Cyborg',
    'Darkly',
    'Flatly',
    'Journal',
    'Litera',
    'Lumen',
    'Lux',
    'Materia',
    'Minty',
    'Morph',
    'Pulse',
    'Quartz',
    'Sandstone',
    'Simplex',
    'Sketchy',
    'Slate',
    'Solar',
    'Spacelab',
    'Superhero',
    'United',
    'Vapor',
    'Yeti',
    'Zephyr',
]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])

# get the data
def starter_vis():
    # function calls for visualization builders
    # Starter for initial dash populating
    pass 

# returned_visual_figures = starter_vis()

fig1 = viz.build_fig_one()

fig2 = viz.build_fig_two()

fig3 = viz.build_fig_three()

fig4 = viz.build_fig_four()

app.layout = html.Div(
    [
        # dcc.Interval(id="interval-component", interval=60 * 1000, n_intervals=0),
        dbc.Row(
            html.H1("Arctic Analysts Starter Dashboard"),
            className = 'text-center'
        ),
        dbc.Row(
            html.Div(id="record_count"),
            className = 'text-center',
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="first",
                        figure=fig1,
                        style={"float": "left", "width": "2", "height": "100%", 'pad': '15'},
                    )
                ), 
                dbc.Col(
                    [
                        dcc.Graph(
                            id="second",
                            figure=fig2,
                            style={"float": "right", "width": "6", "height": "50%"},
                        ),
                        dcc.Graph(
                            id="third",
                            figure=fig3,
                            style={"float": "right", "width": "6", "height": "50%"},
                        ),
                    ]
                ),
            ],
            className='h-75',
        ),
        dbc.Row(
            [
                dcc.Graph(
                    id="fourth",
                    figure=fig4,
                    style={"float": "right", "width": "12", "height": "25%"},
                )
            ],
            className="h-25",
        ),
    ]
)


# @app.callback(
#     Output("first", "figure"),
#     Output("second", "figure"),
#     Output("third", "figure"),
#     Output("fourth", "figure"),
#     Output("record_count", "children"),
#     Input("interval-component", "n_intervals"),
# )
# def get_data_and_visualize(n):
#     # function calls for visualization builders
#     pass


if __name__ == "__main__":
    # print('Would Normally Run the Dashboard now, but not ready yet.')
    app.run_server(debug=True)
