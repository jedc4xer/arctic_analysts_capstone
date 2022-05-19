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

PAGE_TEXT_CONTENT_1 = """
Home ownership is a goal of many Americans, and recent years have seen the price of homes increase rapidly.
Our question, given a select group of conditions, to what extent can we predict near term affordability of homes
for the typical American Household. We are specifically focusing on counties in the state of New Jersey. 
"""

PAGE_TEXT_CONTENT_2 = "The factors that we are using to inform our prediction are:"

PAGE_TEXT_CONTENT_3a = "   - Median Income"
PAGE_TEXT_CONTENT_3b = "   - Construction of New Housing"
PAGE_TEXT_CONTENT_3c = "   - Average Mortgage Interest Rate"
PAGE_TEXT_CONTENT_3d = "   - Median House Prices"

PAGE_TEXT_CONTENT_4 = """
Our prediction will involve forecasting the income, new housing, mortgage interest rate, and median house prices for all counties, and then taking those results and classifying each county as affordable or not affordable.

"""

PAGE_TEXT_CONTENT_5 = """
We are defining home affordability as when the monthly mortgage payment is equal to or less than 25% of the monthly median income given a 20% down-payment.
"""

PAGE_TEXT_CONTENT_6 = """
A county will be considered affordable if a household making the median income will be able to afford a home that is a median priced home in that county.
"""

list_group = (
    dbc.ListGroup(
        [
            dbc.ListGroupItem(PAGE_TEXT_CONTENT_3a),
            dbc.ListGroupItem(PAGE_TEXT_CONTENT_3b),
            dbc.ListGroupItem(PAGE_TEXT_CONTENT_3c),
            dbc.ListGroupItem(PAGE_TEXT_CONTENT_3d),
        ]
    ),
)

HOMEPAGE_LAYOUT = html.Div(
    [
        # dbc.Row(html.H1("New Jersey Housing Analysis"), className="text-center"),
        dbc.Row(
            [
                dbc.Col(width="3"),
                dbc.Col(
                    [
                        dbc.Row(html.H3("Analysis Summary"), className="text-center",),
                        dbc.Row(html.P(PAGE_TEXT_CONTENT_1), className="text-left"),
                        dbc.Row(html.P(PAGE_TEXT_CONTENT_2), className="text-left"),
                        dbc.Row(
                            [
                                dbc.Col(html.P(list_group, style={"padding": "10px"}),),
                                dbc.Col(),
                            ]
                        ),
                        dbc.Row(html.P(PAGE_TEXT_CONTENT_4), className="text-left"),
                        dbc.Row(html.P(PAGE_TEXT_CONTENT_5), className="text-left"),
                        dbc.Row(html.P(PAGE_TEXT_CONTENT_6), className="text-left"),
                    ]
                ),
                dbc.Col(width="3"),
            ],
            # className="h-25",#
        ),
    ]
)
