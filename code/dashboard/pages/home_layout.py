import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

# This code basically adds padding to the top, bottom, and both sides of the screen
CONTENT_STYLE = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "1rem 1rem",
}

THEMES = {
    "CERULEAN": dbc.themes.CERULEAN,
    "COSMO": dbc.themes.COSMO,
    "CYBORG": dbc.themes.CYBORG,
    "DARKLY": dbc.themes.DARKLY,
    "FLATLY": dbc.themes.FLATLY,
    "JOURNAL": dbc.themes.JOURNAL,
    "LITERA": dbc.themes.LITERA,
    "LUMEN": dbc.themes.LUMEN,
    "LUX": dbc.themes.LUX,
    "MATERIA": dbc.themes.MATERIA,
    "MINTY": dbc.themes.MINTY,
    "MORPH": dbc.themes.MORPH,
    "PULSE": dbc.themes.PULSE,
    "QUARTZ": dbc.themes.QUARTZ,
    "SANDSTONE": dbc.themes.SANDSTONE,
    "SIMPLEX": dbc.themes.SIMPLEX,
    "SKETCHY": dbc.themes.SKETCHY,
    "SLATE": dbc.themes.SLATE,
    "SOLAR": dbc.themes.SOLAR,
    "SPACELAB": dbc.themes.SPACELAB,
    "SUPERHERO": dbc.themes.SUPERHERO,
    "UNITED": dbc.themes.UNITED,
    "VAPOR": dbc.themes.VAPOR,
    "YETI": dbc.themes.YETI,
    "ZEPHYR": dbc.themes.ZEPHYR,
}

# To test a theme, change the name of the theme, save, and then refresh the dashboard.
__current_theme = "QUARTZ"
THEME = THEMES[__current_theme]

HOMEPAGE_LAYOUT = html.Div(
    [
        dbc.Row(html.H1("US Housing Analysis"), className="text-center"),
        dbc.Row(
            html.H3("Possibly Include an Executive Summary or other content here."),
            className="text-center",
        ),
        dbc.Row(html.P("Or Here, could work also."), className="text-center"),
    ]
)
