import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from config import tight_shadow, shadow

# This code basically adds padding to the top, bottom, and both sides of the screen

PHILS_BIO = [
    "Phil is a graduate of Rutgers University with a Bachelor's Degree in Philosophy and Human Psychology.",
    html.Br(),
    html.Br(),
    "You can usually find Phil in the Blue Room at the Guthrie Theatre, or meeting with his Underwater Basket Weaving club members discussing new techniques for creating intricate aqua-baskets.",
]
JEDS_BIO = [
    "Jed is a graduate of Arizona State University with a Bachelor's Degree in Business Sustainability.",
    html.Br(),
    html.Br(),
    "You can usually find Jed either writing code or enjoying the warmth of summer. He loves to spend his spare time with family and finding new adventures.",
]
HANS_BIO = [
    "Han is a graduate of Hamline University with a Bachelor's Degree in Sociology, and University of St. Thomas with a Master's Degree in Data Science.",
    html.Br(),
    html.Br(),
    "You can usually find Han exploring the Minneapolis Art District on Central Avenue, or meeting with Phil's Underwater Basket Weaving club members discussing new techniques for creating intricate aqua-baskets.",
]


ABOUT_US_LAYOUT = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.A(
                            [
                                dbc.Row(
                                    html.H1("Phil Carbino", className="text-center")
                                ),
                                dbc.Row(
                                    html.Center(
                                        html.Img(
                                            src="https://media-exp1.licdn.com/dms/image/C4E03AQGW9CelJ52NFQ/profile-displayphoto-shrink_200_200/0/1645651861405?e=1658966400&v=beta&t=I4mVkicq5psKAzVPLy9kUaq7r3eIkHS_B3RbEtfvIgE",
                                            style={"width": "40%"},
                                        )
                                    )
                                ),
                                dbc.Row(html.P(PHILS_BIO), style={"padding": "30px"}),
                            ],
                            href="https://www.linkedin.com/in/phil-carbino-01941761/",
                            style={"textDecoration": "none"},
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.A(
                            [
                                dbc.Row(html.H1("Jed Dryer", className="text-center")),
                                dbc.Row(
                                    html.Center(
                                        html.Img(
                                            src="https://media-exp1.licdn.com/dms/image/C5603AQEkAhoIEvugGQ/profile-displayphoto-shrink_200_200/0/1627239661413?e=1658966400&v=beta&t=E0OnC1kVT-8TqrQykx7VurNuBnvnuUVqjSbcbckk2iA",
                                            style={"width": "40%"},
                                        )
                                    )
                                ),
                                dbc.Row(html.P(JEDS_BIO), style={"padding": "30px"}),
                            ],
                            href="https://www.linkedin.com/in/jed-dryer/",
                            style={"textDecoration": "none"},
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.A(
                            [
                                dbc.Row(html.H1("Han Luong", className="text-center")),
                                dbc.Row(
                                    html.Center(
                                        html.Img(
                                            src="https://media-exp1.licdn.com/dms/image/C4E03AQEULiM4FST8-w/profile-displayphoto-shrink_200_200/0/1552682173061?e=1658966400&v=beta&t=Eio3s3b3-1FFia5QfrwjSCUolMB2pJKWZ9ob9r7-qUA",
                                            style={"width": "40%"},
                                        )
                                    )
                                ),
                                dbc.Row(html.P(HANS_BIO), style={"padding": "30px"}),
                            ],
                            href="https://www.linkedin.com/in/hanluong/",
                            style={"textDecoration": "none"},
                        ),
                    ]
                ),
            ]
        )
    ],
)
