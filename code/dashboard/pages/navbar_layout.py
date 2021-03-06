import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

NAVIGATION_BAR = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Home Affordability | New Jersey", className="ms-2"
                            )
                        ),
                    ],
                    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                    align="center",
                ),
                href="https://www.nj.gov/njhrc/",
                style={"textDecoration": "none"},
            ),
            dbc.Col(width=3),
            dbc.Col(
                dbc.Nav(
                    dbc.NavLink("Home", href="/", active="exact"), pills=True, fill=True
                )
            ),
            dbc.Col(
                dbc.Nav(
                    dbc.NavLink("Analysis", href="/page-1", active="exact"),
                    pills=True,
                    fill=True,
                )
            ),
            dbc.Col(
                dbc.Nav(
                    dbc.NavLink("Map Visuals", href="/page-2", active="exact"),
                    pills=True,
                    fill=True,
                )
            ),
            dbc.Col(
                dbc.Nav(
                    dbc.NavLink("ML Models", href="/page-3", active="exact"),
                    pills=True,
                    fill=True,
                )
            ),
            dbc.Col(
                dbc.Nav(
                    dbc.NavLink("About Us", href="/page-4", active="exact"),
                    pills=True,
                    fill=True,
                )
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(id="navbar-collapse", is_open=False, navbar=True,),
        ]
    ),
    color="dark",
    dark=True,
)
