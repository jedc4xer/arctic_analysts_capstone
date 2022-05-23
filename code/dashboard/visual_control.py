import json
import time
import functools
import numpy as np
import pandas as pd
import datetime as dt
import plotly.express as px

# import data_control as data_con # Deprecated
import new_data_control as new_data_con
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import counties, feature_options, locale_options, age_groups


# Visual Formatting Functions
##################################


def map_colors():
    """ This returns a color map for functions plotting age group information. """
    color_map = {
        "45-64": "#FF0000",
        "25-44": "#2700FF",
        "overall": "#00A9FF",
        "65-plus": "#E36300",
        "under-25": "#FF00D1",
    }
    return color_map


def format_active_graph_visual(fig, min_range=None, max_range=None, units=None):
    """ This function formats the animated visuals. """
    fig.update_layout(
        paper_bgcolor="rgba(255,255,255,.95)",
        plot_bgcolor="rgba(255,255,255,1)",
        font_color="black",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(1,0,0,0)"},
        dragmode=False,
        xaxis_title=None,
        margin={"r": 8, "t": 50, "l": 5, "b": 15},
    )

    fig.update_xaxes(
        showgrid=False,
        showline=True,
        ticks="outside",
        tickwidth=1,
        ticklen=7,
        tickcolor="rgba(0,0,0,1)",
        tickfont=dict(size=14),
    )

    if units == "Year":
        fig.update_xaxes(range=[2000, 2022])

    fig.update_yaxes(
        showgrid=False,
        showline=True,
        # range = [0,400000],
        ticks="outside",
        tickwidth=1,
        ticklen=6,
        tickcolor="rgba(0,0,0,1)",
        tickfont=dict(size=14),
        tickprefix="$",
    )

    if min_range is not None and min_range >= 0:
        fig.update_yaxes(
            range=[min_range - (min_range * 0.1), max_range + (max_range * 0.1)],
        )
    return fig

# END VISUAL FORMATTING
####################################################


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

# END POLYNOMIAL VISUALS
####################################################


# BLANKS
#########################################3

def blank():
    return px.line()

# END BLANKS
############################################


# ARIMA VISUALIZATIONS
############################################


def arima_visual_controller(df, target, params):

    # df = new_data_con.get_model(target, params)
    try:
        fig = plot_arima_predictions(df, target)
    except Exception as E:
        print(E)
    return fig


def plot_arima_predictions(df, target):

    df["Year"] = df.Year.astype("int")
    trace1 = px.line(x=df["Year"], y=df["full_results"])

    trace1.update_traces(line=dict(color="black", width=3, dash="dash"))
    # trace2.update_traces(line=dict(color="black", width=3))

    fig = go.Figure()
    trace2 = go.Scatter(
        x=df["Year"],
        y=df["MedianIncome"],
        fill="tozeroy",
        hoveron="points+fills",
        fillcolor="lightgrey",
        name="Median Income",
        text=f"Median Income for county",
        hoverinfo="text",
    )
    fig.add_traces(trace2)
    fig.add_traces(trace1.data)
    fig.add_vrect(
        x0=2019,
        x1=2022.5,
        fillcolor="green",
        opacity=0.3,
        line_width=0,
        annotation_text="Goal Data",
        annotation_position="left",
    )

    fig = format_active_graph_visual(fig)

    fig.update_layout(
        showlegend=True,
        title=dict(text="ARIMA Predicted Vs. Actual", font=dict(size=22),),
    )

    return fig


def old_arima_visual_controller(arima_gen, target, locale, age_group):

    # df, differenced_df, arima_step = arima_gen.send([target, [locale, age_group]])
    df, arima_step = arima_gen.send([target, [locale, age_group]])

    df["Year"] = df["Year"].astype("str")
    df.index = df.index.astype("str")

    fig1 = build_differencing_chart(df, target)
    # fig2 = build_arima_visual(df, target)
    print("Ready for fig display")
    return fig1  # , fig2


def build_differencing_chart(df, target):
    fig = make_subplots(rows=3, cols=1)

    fig.append_trace(
        go.Scatter(x=df["Year"], y=df[target], marker=dict(color="white", size=3)),
        row=1,
        col=1,
    )

    fig.append_trace(
        go.Scatter(x=df["Year"], y=df["diff_1"], marker=dict(color="red", size=3)),
        row=2,
        col=1,
    )

    fig.append_trace(
        go.Scatter(x=df["Year"], y=df["diff_2"], marker=dict(color="red", size=3)),
        row=3,
        col=1,
    )

    fig = format_active_graph_visual(
        fig, min_range=False, max_range=False, units="False"
    )

    fig.update_layout(
        title=dict(text="Differenced Data", font=dict(size=22),),
        margin={"r": 10, "t": 50, "l": 5, "b": 25},
        showlegend=False,
    )

    return fig


def build_arima_visual(df, target):

    # try:
    #     df, arima_step = next(arima_gen)
    # except Exception as E:
    #     print('differencing error', E)

    # df['Year'] = df['Year'].astype('str')
    # df.index = df.index.astype('str')
    print(df.columns)
    trace1 = px.line(x=df["Year"], y=df["converted"])
    trace2 = px.line(x=df["Year"], y=df["MedianIncome"])

    fig = go.Figure(data=trace1.data + trace2.data)
    fig = format_active_graph_visual(
        fig, min_range=False, max_range=False, units="False"
    )
    return fig
# END ARIMA VISUALS
####################################################


# ANALYSIS PAGE VISUALS
#####################################################


def income_visual_master(yearly_income, target_fips):

    try:
        full, df = next(yearly_income)
    except Exception as E:
        print(E)
    # new_data_con.highest_median_income()

    min_range = 0
    max_range = full[(full.FIPS == target_fips)]["MedianIncome"].max()
    full = None

    filtered = df[(df.FIPS == target_fips)]

    try:
        args = [min_range, max_range, locale_options[target_fips]]

        fig1 = income_by_age_group(filtered, args)
        fig2 = build_average_median_income(df)
    except Exception as E:
        print(E)

    return fig1, fig2


def home_price_visual_master(home_prices, target_fips):

    full, df = next(home_prices)
    min_range = 0
    max_range = full[(full.FIPS == target_fips)]["MedianHousePrice"].max()
    full = None
    df = df[(df.FIPS == target_fips)]

    args = [min_range, max_range, locale_options[target_fips]]

    fig3 = build_fig_three(df, args)
    return fig3


def income_by_age_group(df, args):
    start = time.perf_counter()

    color_map = map_colors()

    traces = []
    age_group_list = df.AgeGroup.unique().tolist()

    trace1 = px.bar(
        x=df["Year"].unique(),
        y=df[(df.AgeGroup == "overall")]["MedianIncome"],
        opacity=0.3,
    )
    traces.append(trace1)
    for age in age_group_list:
        if age == "overall":
            continue

        trace = px.line(
            x=df["Year"].unique(),
            y=df[(df.AgeGroup == age)]["MedianIncome"],
            # color=df["AgeGroup"],
            # color_discrete_map=color_map,
        )
        trace.update_traces(line=dict(color=color_map[age], width=3, dash="dash"))
        trace.update_traces(name=age_groups[age])
        traces.append(trace)

    fig = go.Figure(
        data=traces[0].data
        + traces[1].data
        + traces[2].data
        + traces[3].data
        + traces[4].data
    )

    max_year = df.dropna().Year.max()
    try:
        fig.add_vrect(
            x0=2000,
            x1=2005,
            fillcolor="red",
            opacity=0.3,
            line_width=0,
            annotation_text="No Data",
            annotation_position="top left",
        )

        fig.add_vrect(
            x0=2019,
            x1=2022,
            fillcolor="red",
            opacity=0.20,
            line_width=0,
            annotation_text="No Data",
            annotation_position="top left",
        )
    except Exception as E:
        print(E)

    # fig.update_traces(line=dict(width=2))
    # fig3.update_traces(line=dict(color="red", width=3, dash="dash"))
    # fig.update_traces(
    #         mode="markers",
    #         marker_line_width=2,
    #         marker_size=10,
    #     )

    min_range, max_range, locale = args
    fig.update_layout(
        title=dict(
            text=f"<b>Median Income by Age Group | {locale}<b>", font=dict(size=20)
        ),
        legend=dict(
            font_color="black",
            title="",
            orientation="h",
            yanchor="top",
            y=1.10,
            xanchor="left",
            x=0.18,
            bgcolor=("rgba(0,0,0,0)"),
        ),
    )
    fig = format_active_graph_visual(fig, min_range, max_range, "Year")
    build_time = round(time.perf_counter() - start, 3)
    return fig


def build_average_median_income(df):
    df = df[(df.AgeGroup != "overall")]
    df = df.groupby(by=["FIPS", "County"])[["MedianIncome"]].agg("mean").reset_index()
    df.sort_values(by="MedianIncome", ascending=True, inplace=True)
    df = df.tail(5)
    fig = px.bar(x=df["MedianIncome"], y=df["County"])
    fig = format_active_graph_visual(fig)
    fig.update_yaxes(tickprefix="")
    fig.update_xaxes(tickprefix="$")
    fig.update_layout(
        title=dict(
            text=f"<b>Counties with Highest Overall Average Median Income<b>",
            font=dict(size=20),
        )
    )
    return fig


def build_fig_one(df, args):

    color_map = map_colors()
    fig = px.line(
        x=df["Year"],
        y=df["MedianIncome"],
        color=df["AgeGroup"],
        color_discrete_map=color_map,
    )

    max_year = df.dropna().Year.max()
    try:
        fig.add_vrect(
            x0=2000,
            x1=2005,
            fillcolor="red",
            opacity=0.3,
            line_width=0,
            annotation_text="No Data",
            annotation_position="top left",
        )

        fig.add_vrect(
            x0=2019,
            x1=2022,
            fillcolor="red",
            opacity=0.20,
            line_width=0,
            annotation_text="No Data",
            annotation_position="top left",
        )
    except Exception as E:
        print(E)

    fig.update_traces(line=dict(width=2))
    # fig3.update_traces(line=dict(color="red", width=3, dash="dash"))
    # fig.update_traces(
    #         mode="markers",
    #         marker_line_width=2,
    #         marker_size=10,
    #     )

    min_range, max_range, locale = args
    fig.update_layout(
        title=dict(
            text=f"<b>Median Income by Age Group | {locale}<b>", font=dict(size=20)
        ),
        paper_bgcolor="rgba(0,0,0,.1)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
        legend=dict(
            title="",
            orientation="h",
            yanchor="top",
            y=1.10,
            xanchor="left",
            x=0.18,
            bgcolor=("rgba(0,0,0,0)"),
        ),
    )
    fig = format_active_graph_visual(fig, min_range, max_range, "Year")
    return fig


def build_fig_two(df, args):
    start = time.perf_counter()
    # df = new_data_con.income_data_generator()
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
    fig = format_active_graph_visual(fig, min_range, max_range, "Year")
    build_time = round(time.perf_counter() - start, 3)
    return fig, build_time


def build_fig_three(df, args):
    df = df.drop_duplicates()
    fig = px.bar(df, x="Date", y="MedianHousePrice", color="FIPS")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,.5)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    min_range, max_range, locale = args

    fig.update_layout(
        title=dict(text=f"<b>Median House Price for {locale}<b>", font=dict(size=20),),
        showlegend=False,
    )

    fig = format_active_graph_visual(fig, min_range, max_range, "Date")
    # print("Here")
    # if min_range:
    #     print("here")
    #     fig.update_yaxes(
    #     range=[min_range - (min_range * 0.1), max_range + (max_range * 0.1)],
    #     )

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

# END ANALYSIS PAGE VISUALS
####################################################


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
    customdata = np.stack((df["County"], df["MedianIncome"], df["AgeGroup"]), axis=-1)

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
        hover_data=["County", "MedianIncome", "AgeGroup"],
    )
    fig.update_traces(
        hovertemplate="<b>County: %{customdata[0]}</b><br>Median Income: %{customdata[1]:$,}<br>Age Group: %{customdata[2]}"
    )
    return fig


def map_builder(
    income_data_for_map,
    base_map_style,
    age_group,
    target_year,
    animate,
    target="MedianIncome",
):

    df = next(income_data_for_map)
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
        print(target_year)
        df = df[(df.Year == target_year) & (df.AgeGroup == age_group)]
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
            titlefont=dict(color="white", size=15),
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

# END MAP VISUALS
####################################################


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
