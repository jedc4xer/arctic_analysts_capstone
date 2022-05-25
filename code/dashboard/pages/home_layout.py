import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from config import tight_shadow, shadow

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
Owning a home is a long-term goal for many Americans, and the trends of recent years have caused many to question their abilitity to purchase a home as prices have increased rapidly. In this analysis, we looked at affordability specifically in New Jersey at the county level. We will use current house prices, the average mortgage interest rate, and forecasted median income to classify counties as affordable or not affordable.
"""

PAGE_TEXT_CONTENT_2 = "The factors that we considered for this analysis were:"

LIST = """
* Median Income | 2005 - 2019
* New Housing Permits | 2000 - 2022
* Average Mortgage Interest Rate | 2000 - 2022
* Median House Prices | 2000 - 2022
"""

PAGE_TEXT_CONTENT_4 = """
We were able to get current data for all of our variables except for Median Income, which was gathered from the US Census ACS and was last updated in 2019. In order to fill in the gaps, we will be using a time-series model on the U.S. Income Data to get a forecast of current income levels. 
"""

PAGE_TEXT_CONTENT_4A = """
We are defining home affordability as when the monthly mortgage payment including the average property tax is less than or equal to 25% of a household's monthly median income given a 12% down-payment.
"""

PAGE_TEXT_CONTENT_5 = """
A county will be considered affordable if a household making the median income will be able to afford a home that is a median priced home in that county.
"""

HOMEPAGE_LAYOUT = html.Div(
    [
        # dbc.Row(html.H1("New Jersey Housing Analysis"), className="text-center"),
        dbc.Row(
            [
                dbc.Col(width="1"),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Row(
                                html.H3("Analysis Summary"), className="text-center",
                            ),
                            dbc.Row(html.P(PAGE_TEXT_CONTENT_1), className="text-left"),
                            dbc.Row(html.P(PAGE_TEXT_CONTENT_2), className="text-left"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Markdown(
                                            LIST,
                                            style={
                                                "padding": "10px",
                                                "box-shadow": "1px 3px 5px 7px lightblue",
                                            },
                                        ),
                                    ),
                                    dbc.Col(width='5'),
                                ]
                            ),
                            dbc.Row(
                                html.P(PAGE_TEXT_CONTENT_4),
                                className="text-left",
                                style={"margin-top": "10px"},
                            ),
                            dbc.Row(
                                html.P(PAGE_TEXT_CONTENT_4A), className="text-left"
                            ),
                            dbc.Row(html.P(PAGE_TEXT_CONTENT_5), className="text-left"),
                        ]
                    ),
                    style={
                        "padding": "10px",
                        "box-shadow": "1px 7px 5px 7px lightgrey",
                    },
                ),
                dbc.Col(width='1'),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Row(style={'margin-top': "35px"}),
                            dbc.Row(html.H5('Summary Statistics')),
                            dbc.Row(html.H6('Number of Counties: 21')),
                            dbc.Row(html.H6('Income Age Brackets: 5')),
                            dbc.Row(html.H6('Average House Price')),
                            dbc.Row(html.P(['2000: $192,086',html.Br(),'2022: $434,143',html.Br(),'Overall: $311,750'])),
                            dbc.Row(html.H6('Average Income')),
                            dbc.Row(html.P(['2005: $55,701',html.Br(),'2019: $77,410',html.Br(),'Overall: $63,866'])),
                            dbc.Row(html.H6('Mortgage Rates')),
                            dbc.Row(html.P(['Average: 4.98%',html.Br(),'Minimum: 2.68%',html.Br(),'Maximum: 8.52%'])),
                        ], style={'box-shadow': '2px 2px 5px 5px lightgrey', 'padding': '0px 20px'}
                    ),
                    width="2"),
                dbc.Col(width='1')
            ],
            # className="h-25",#
        ),
    ],
)
