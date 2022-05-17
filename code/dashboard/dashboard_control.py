import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from pages.navbar_layout import *  # Importing all the variables from the navbar_layout file
from pages.analysis_layout import ANALYSIS_LAYOUT
from pages.map_layout import MAP_LAYOUT
from pages.test_layout import TEST_LAYOUT
from pages.models_layout import MODEL_LAYOUT
from pages.home_layout import *

print("\nThe program has just passed through the first line of dashboard_control.py\n")

app = dash.Dash(
    __name__, external_stylesheets=[THEME], suppress_callback_exceptions=True
)

navbar = NAVIGATION_BAR
content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([dcc.Location(id="url"), navbar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        print("Picked Home Page")
        return HOMEPAGE_LAYOUT

    elif pathname == "/page-1":
        print("Picked Analysis Page")
        return ANALYSIS_LAYOUT

    elif pathname == "/page-2":
        print("Picked Map Page")
        print("This may take about 15 seconds to load at the moment.")
        return MAP_LAYOUT

    elif pathname == "/page-3":
        print("Picked ML Model Page")
        return MODEL_LAYOUT

    elif pathname == "/page-4":
        print("Picked Test Page")
        return TEST_LAYOUT

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
