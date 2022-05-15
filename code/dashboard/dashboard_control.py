import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from pages.navbar_layout import *  # Importing all the variables from the navbar_layout file
from pages.analysis_layout import ANALYSIS_LAYOUT
from pages.map_layout import MAP_LAYOUT
from pages.home_layout import *

print("Here again at home base.")

app = dash.Dash(
    __name__, external_stylesheets=[THEME], suppress_callback_exceptions=True
)

navbar = NAVIGATION_BAR
content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([dcc.Location(id="url"), navbar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return HOMEPAGE_LAYOUT

    elif pathname == "/page-1":
        return ANALYSIS_LAYOUT

    elif pathname == "/page-2":
        return MAP_LAYOUT

    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")

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
