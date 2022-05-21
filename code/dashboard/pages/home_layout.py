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
In this analysis, we are attempting to predict the affordability of homes using a select group of conditions.

We are specifically focusing on counties in the state of New Jersey. 
"""

PAGE_TEXT_CONTENT_2 = "The factors that we are using to inform our predictions are:"

PAGE_TEXT_CONTENT_3a = "   - Median Income"
PAGE_TEXT_CONTENT_3b = "   - Construction of New Housing"
PAGE_TEXT_CONTENT_3c = "   - Average Mortgage Interest Rate"
PAGE_TEXT_CONTENT_3d = "   - Median House Prices"

LIST = """
* Median Income
* New Housing Permits
* Average Mortgage Interest Rate
* Median House Prices
"""

PAGE_TEXT_CONTENT_4 = """
We were able to get current data for all of our features except for income, which was last updated in 2019. The income data is also 
based on annual income while our other data is monthly. This means that our error margin for income will be relatively high and could
result in some unrealistic predictions. 
"""

PAGE_TEXT_CONTENT_4A = """
In order to make our predictions, we are using an ARIMA model for time series predictions. We then do a simple calculation based on the results.
"""

PAGE_TEXT_CONTENT_5 = """
We are defining home affordability as when the monthly mortgage payment including the average property tax is less than or equal to 25% of a household's monthly median income given a 20% down-payment.
"""

PAGE_TEXT_CONTENT_6 = """
A county will be considered affordable if a household making the median income will be able to afford a home that is a median priced home in that county.
"""

# list_group = (
#     dbc.ListGroup(
#         [
#             dbc.ListGroupItem(PAGE_TEXT_CONTENT_3a),
#             dbc.ListGroupItem(PAGE_TEXT_CONTENT_3b),
#             dbc.ListGroupItem(PAGE_TEXT_CONTENT_3c),
#             dbc.ListGroupItem(PAGE_TEXT_CONTENT_3d),
#         ]
#     ),
# )

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
                                dbc.Col(dcc.Markdown(LIST, style={"padding": "10px"}),),
                                dbc.Col(),
                            ]
                        ),
                        dbc.Row(html.P(PAGE_TEXT_CONTENT_4), className="text-left"),
                        dbc.Row(html.P(PAGE_TEXT_CONTENT_4A), className="text-left"),
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
