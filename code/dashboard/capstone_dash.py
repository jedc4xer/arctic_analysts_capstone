import dash
from dash import dcc, html
import data_control as data_con
import visualization_builder as viz
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# I think I have to put any dynamic chart data gathering below
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
def get_data():
    data_dict = data_con.prepare_data()
    return data_dict

def starter_vis(data_dict):
    # function calls for visualization builders
    # Starter for initial dash populating
    fig1 = viz.build_fig_one()

    fig2 = viz.build_fig_two()

    fig3 = viz.build_fig_three(data_dict['median_income'])
    
    fig4 = viz.build_fig_four(data_dict['house_prices'])
    
    #fig4 = viz.build_fig_four()
    
    return fig1, fig2, fig3, fig4



app.layout = html.Div(
    [
        dcc.Interval(id="interval-component", interval=3 * 1000, n_intervals=0),
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
                        #figure=fig1, For a static graph I believe this is useful
                        style={"padding": '10px', "border-radius": '20px', "float": "left", "width": "2", "height": "50vh"},
                    )
                ), 
                dbc.Col(
                    [
                        dcc.Graph(
                            id="second",
                            style={"padding": '10px', "float": "right", "width": "6", "height": "25vh"},
                        ),
                        dcc.Graph(
                            id="third",
                            style={"padding": '10px', "float": "right", "width": "6", "height": "25vh"},
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
                    style={"padding": '10px', "float": "right", "width": "12", "height": "40vh"},
                )
            ],
            className="h-25",
        ),
    ]
)


@app.callback(
      Output("first", "figure"),
      Output("second", "figure"),
      Output("third", "figure"),
      Output("fourth", "figure"),
#     Output("record_count", "children"),
      Input("interval-component", "n_intervals"),
)
def get_data_and_visualize(n):
    
    # Get the Data
    data_dict = get_data()

    # Send the Data to the Visual Builder
    fig1, fig2, fig3, fig4 = starter_vis(data_dict)
    
    #fig4 = viz.build_fig_four(data_dict['house_prices'])
    return fig1, fig2, fig3, fig4


if __name__ == "__main__":
    # print('Would Normally Run the Dashboard now, but not ready yet.')
    
    app.run_server(debug=True)
