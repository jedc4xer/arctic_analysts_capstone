import json
import time
import functools
import pandas as pd
import datetime as dt
import plotly.express as px
import data_control as data_con
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import counties, feature_options, locale_options


# Visual Formatting Functions
##################################


def map_colors():
    """ This returns a color map for functions plotting age group information. """
    color_map = {
        "45-64": "#00FCDE",
        "25-44": "#D90CF0",
        "overall": "#001AD9",
        "65-plus": "#FAAF01",
        "under-25": "#D92C00",
    }
    return color_map


def format_active_graph_visual(fig, min_range, max_range):
    """ This function formats the animated visuals. """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,.1)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(1,0,0,0)"},
        dragmode=False,
    )

    fig.update_xaxes(
        showgrid=False,
        showline=True,
        ticks="outside",
        tickwidth=1,
        ticklen=7,
        tickcolor="rgba(255,255,255,1)",
    )
    fig.update_yaxes(
        showgrid=False,
        showline=True,
        range=[min_range - (min_range * 0.1), max_range + (min_range * 0.1)],
        # range = [0,400000],
        ticks="outside",
        tickwidth=1,
        ticklen=6,
        tickcolor="rgba(255,255,255,1)",
    )
    return fig


# Build Model Visualizations
####################################


def build_polynomial_model(model_data, target, locale, best):
    """ This function creates a visualization for a polynomial regression model. """

    # This data was returned from a generator yield on the MODEL_LAYOUT page.
    # It is yielded from the poly_generator in the data_control.py file
    # It is received in a list and unpacked in the code below.
    try:
        i, predictions, original, futures = model_data
    except Exception as E:
        print("Error in build_polynomial_model", E)

    # Get the dates for the predictions
    freq = "M" if target != "MedianIncome" else "Y"
    num_periods = futures.shape[0]
    fixed_dates = data_con.get_date_range(
        original["date"].dropna().tolist()[-1], num_periods, freq
    )

    # Add the prediction dates to the prediction df
    futures["date"] = fixed_dates

    # combine all the dataframes
    data_for_plotting = pd.merge(
        original, predictions, left_on="predictor", right_on="x_var", how="outer"
    )
    data_for_plotting = pd.merge(
        data_for_plotting,
        futures,
        left_on=["predictor", "date"],
        right_on=["predictor", "date"],
        how="outer",
    )
    data_for_plotting["date"] = pd.to_datetime(data_for_plotting["date"])

    # Create the first trace
    if target == "MedianIncome":
        fig1 = px.scatter(x=data_for_plotting["date"], y=data_for_plotting[target])
        fig1.update_traces(
            mode="markers",
            marker_line_width=2,
            marker_size=15,
            marker_color="rgba(0,0,255,.3)",
        )

    else:
        fig1 = px.line(x=data_for_plotting["date"], y=data_for_plotting[target])
        fig1.update_traces(line=dict(color="black", width=3))

    # Create the second trace
    fig2 = px.line(x=data_for_plotting["date"], y=data_for_plotting["predictions"])

    fig3 = px.line(x=data_for_plotting["date"], y=data_for_plotting["futures"])

    fig2.update_traces(line=dict(color="white", width=3, dash="dash"))
    fig3.update_traces(line=dict(color="red", width=3, dash="dash"))

    # Combine the traces into a single figure
    final_fig = go.Figure(data=fig1.data + fig2.data + fig3.data)

    if best:
        indicate_best = "| Lowest RMSE | (Animation Paused)"
    else:
        indicate_best = ""

    title_string = f"""
    <b>{feature_options[target]} | Degrees: {i}<br>
    {locale_options[locale]} {indicate_best}<b>
    """
    # Add and format the title
    final_fig.update_layout(title=dict(text=title_string, font=dict(size=20),))

    min_range = original[target].min()
    max_range = original[target].max()

    # Send the figure out for formatting.
    final_fig = format_active_graph_visual(final_fig, min_range, max_range)
    return final_fig


def income_visual_master(yearly_income, target_fips):

    full, df = next(yearly_income)
    min_range = 0
    max_range = full[(full.FIPS == target_fips)]["MedianIncome"].max()
    full = None
    df = df[(df.FIPS == target_fips)]

    args = [min_range, max_range, locale_options[target_fips]]
    fig1, fig1_time = build_fig_one(df, args)
    fig2, fig2_time = build_fig_two(df, args)

    if fig1_time > 0.2 or fig2_time > 0.2:
        print(
            f"{fig1_time} seconds to build line chart | {fig2_time} seconds to build bottom chart"
        )
    return fig1, fig2


def build_fig_one(df, args):
    start = time.perf_counter()

    color_map = map_colors()
    fig = px.line(
        x=df["Year"],
        y=df["MedianIncome"],
        color=df["AgeGroup"],
        color_discrete_map=color_map,
    )

    fig.update_traces(line=dict(width=3))

    min_range, max_range, locale = args
    fig.update_layout(
        title=dict(
            text=f"<b>Median Income by Age Group | {locale}<b>", font=dict(size=20)
        ),
        paper_bgcolor="rgba(0,0,0,.1)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    fig = format_active_graph_visual(fig, min_range, max_range)
    build_time = round(time.perf_counter() - start, 3)
    return fig, build_time


def build_fig_two(df, args):
    start = time.perf_counter()
    color_map = map_colors()
    fig = px.bar(
        x=df["Year"],
        y=df["MedianIncome"],
        color=df["AgeGroup"],
        barmode="group",
        color_discrete_map=color_map,
    )

    min_range, max_range, locale = args
    fig.update_layout(
        title=dict(
            text=f"<b>Median Income by Age Group for {locale}<b>", font=dict(size=20),
        ),
    )
    fig = format_active_graph_visual(fig, min_range, max_range)
    build_time = round(time.perf_counter() - start, 3)
    return fig, build_time


def build_fig_three(income_df):
    fig = px.bar(income_df, x="year", y="MedianIncome", color="StateFips")
    fig.update_layout(
        title=dict(text="<b>Chart 3<b>", font=dict(size=20)),
        paper_bgcolor="rgba(0,0,0,.5)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    fig.update_xaxes(ticks="outside", tickwidth=1, ticklen=7, tickcolor="rgba(0,0,0,0)")
    fig.update_yaxes(ticks="outside", tickwidth=1, ticklen=6, tickcolor="rgba(0,0,0,0)")
    return fig


def build_fig_four():

    print("\nBuilding Median Income by Age Group chart.")
    df = data_con.income_data()

    fig = px.bar(
        x=df["Year"], y=df["MedianIncome"], color=df["AgeGroup"], barmode="group"
    )
    fig.update_layout(
        title=dict(text="<b>Median Income by Age Group<b>", font=dict(size=20)),
        paper_bgcolor="rgba(0,0,0,.2)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,0)"},
    )
    fig.update_xaxes(ticks="outside", tickwidth=1, ticklen=7, tickcolor="rgba(0,0,0,0)")
    fig.update_yaxes(ticks="outside", tickwidth=1, ticklen=6, tickcolor="rgba(0,0,0,0)")
    print("Finished Building Median Income by Age Group Chart\n")
    return fig


def build_income_line_chart(income_df):
    """ This function builds a filled area chart (which can be easily turned into a line chart)"""

    fig = px.line(income_df, x="Year", y="MedianIncome", color="FIPS")

    fig.update_layout(
        title=dict(text="<b>Chart 4<b>", font=dict(size=20)),
        paper_bgcolor="rgba(255,255,255,1)",
        plot_bgcolor="rgba(255,255,255,1)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    fig.update_xaxes(ticks="outside", tickwidth=1, ticklen=7, tickcolor="rgba(0,0,0,0)")
    fig.update_yaxes(ticks="outside", tickwidth=1, ticklen=6, tickcolor="rgba(0,0,0,0)")

    return fig


# Map Visualizations
###################################


def format_map_menu(fig):
    # First removing the current buttons
    fig["layout"].pop("updatemenus")

    # Updating the slider appearance
    fig["layout"]["sliders"][0]["visible"] = True
    fig["layout"]["sliders"][0]["len"] = 0.75
    fig["layout"]["sliders"][0]["x"] = 0.15
    fig["layout"]["sliders"][0]["currentvalue"]["font"]["color"] = "rgba(0,0,0,0)"
    fig["layout"]["sliders"][0]["yanchor"] = "bottom"
    fig["layout"]["sliders"][0]["activebgcolor"] = "rgba(0,0,0,0)"
    fig["layout"]["sliders"][0]["bgcolor"] = "rgba(0,0,0,1)"
    fig["layout"]["sliders"][0]["bordercolor"] = "rgba(0,0,0,1)"
    fig["layout"]["sliders"][0]["font"]["color"] = "black"
    fig["layout"]["sliders"][0]["font"]["size"] = 14

    # Adding a new button and modifying the behavior.
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=True,
                y=0,
                x=0,
                xanchor="left",
                yanchor="bottom",
                pad=dict(b=20, r=10),
                font=dict(size=18),
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=200, redraw=True),
                                transition=dict(duration=0),  # linear
                                fromcurrent=True,
                                mode="immediate",
                            ),
                        ],
                    )
                ],
            )
        ]
    )

    return fig


def build_animated_map(df, base_map_style, scale, animate):
    fig = px.choropleth_mapbox(
        df,
        geojson=counties,
        color="MedianIncome",
        locations="FIPS",
        featureidkey="properties.FIPSSTCO",
        center={"lat": 40.15, "lon": -74.421983},
        mapbox_style=base_map_style,
        zoom=6.5,
        opacity=0.8,
        animation_frame=animate,
        range_color=scale,
        color_continuous_scale="jet",
    )
    return fig


def map_builder(base_map_style, age_group, animate, target="MedianIncome"):

    df = data_con.income_data()
    df = df[(df[target] > 0)]
    df = df.drop(columns=["Month", "MedianHousePrice"])

    if animate == "animated":
        print("Building Animated Map")
        df = df[(df.AgeGroup == age_group)]
        scale = [df[target].min(), df[target].max()]
        df.drop_duplicates(inplace=True)
        df = df.sort_values(by="Year")

        fig = build_animated_map(df, base_map_style, scale, "Year")
        fig = format_map_menu(fig)
    else:
        print("Building Static Map")
        df = df[(df.Year == 2019) & (df.AgeGroup == age_group)]
        scale = [df[target].min(), df[target].max()]
        df = df.drop_duplicates()
        fig = build_animated_map(df, base_map_style, scale, None)

    # if animate == 'animated':
    #     slider_data = fig['layout']['sliders'][0]
    #     print(f"active:{slider_data['active']} value:{slider_data['steps'][slider_data['active']]['args'][0][0]}")

    fig.update_layout(
        coloraxis_showscale=True,
        title=dict(text=f"<b>{'Median Income'}<b>", font=dict(size=28)),
        margin={"r": 0, "t": 0, "l": 0, "b": 0, "autoexpand": True},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="black",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    fig.update_layout(
        title_y=0.96,
        title_x=0.05,
        legend=dict(x=0.9, y=0.4),
        coloraxis_colorbar=dict(
            title=f"{feature_options[target]}",
            ticks="inside",
            ticklen=24,
            thickness=25,
            tickcolor="white",
            tickfont=dict(color="white", size=14),
            tickprefix="$",
            len=0.85
            #             thicknessmode="pixels", thickness=25,
            #             lenmode="fraction", len=.5,
            #             yanchor="top", y=.75,
            #             ticks="outside", ticksuffix=" bills",
            #             #dtick=100000
        ),
    )

    print("Finished Building Median Income Choropleth Map")
    return fig


# Possible Trash
##########################################33

# def build_static_map_one():

#     df = data_con.age_filtered_data()
#     print("Building Median Home Price Choropleth Map")

#     fig = px.choropleth(
#         df,
#         geojson=counties,
#         color="MedianHousePrice",
#         locations="FIPS",
#         featureidkey="properties.FIPSSTCO",
#         #animation_frame="date",
#     )

#     fig.update_geos(
#         fitbounds="locations",
#         visible=False,
#         bgcolor="rgba(0,0,0,0)",
#         resolution=50,
#         landcolor="lightgrey",
#         subunitcolor="black",
#     )

#     fig.update_layout(
#         coloraxis_showscale=True,
#         title=dict(text=f"<b>{'Median Home Prices'}<b>", font=dict(size=20)),
#         margin={"r": 0, "t": 0, "l": 0, "b": 0},#, "autoexpand": True},
#         height=800,
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         font_color="white",
#         modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
#     )
#     fig.update_layout(
#         title_y=1,
#         title_x=0.25,
#         title_font_size=18,
#         legend=dict(x=0.6, y=0.4),
#         coloraxis_colorbar=dict(
#             title="Number of Bills per Cell",
#             thicknessmode="pixels", thickness=25,
#             lenmode="fraction", len=.5,
#             yanchor="top", y=.75,
#             ticks="outside", ticksuffix=" bills",
#             #dtick=100000
#         )
#     )

#     print("Finished Building Median Home Price Choropleth Map")
#     return fig
