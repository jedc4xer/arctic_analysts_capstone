import dash

from pages.home_layout import *
from pages.navbar_layout import *
from pages.map_layout import MAP_LAYOUT

import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from pages.models_layout import MODEL_LAYOUT
from pages.analysis_layout import ANALYSIS_LAYOUT

# Initialize Dashboard
#################################

app = dash.Dash(
    __name__,
    external_stylesheets=[THEME],
    suppress_callback_exceptions=True,
    title="Dash",
    update_title=None,
)

navbar = NAVIGATION_BAR
content = html.Div(id="page-content", style=CONTENT_STYLE)

# Assign Layout
##################################

app.layout = html.Div([dcc.Location(id="url"), navbar, content])


# This callback function determines what to do when different navbar links are clicked.
@app.callback(
    Output("page-content", "children"), [Input("url", "pathname")],
)
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

    # elif pathname == "/page-4":
    #     print("Picked Test Page")
    #     return TEST_LAYOUT

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.H3("Really???"),
            html.H3(f" You are going to have to do better than {pathname}."),
        ],
        className="text-center",
    )


if __name__ == "__main__":
    app.run_server(debug=True)
