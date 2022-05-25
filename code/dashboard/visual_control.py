import json
import time
import functools
import numpy as np
import pandas as pd
import datetime as dt
import plotly.express as px
import arima_model as arima
import plotly.graph_objects as go
import new_data_control as new_data_con
from plotly.subplots import make_subplots
from config import counties, feature_options, locale_options, age_groups, mode


#################################
# VISUAL FORMATTING
#################################


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


def format_active_layout(fig):
    """ This function formats the layout of a figure. """
    if mode == "normal":
        paper = "rgba(255,255,255,.95)"
        plot_bg = "rgba(255,255,255,0)"
        font_color = "black"
    elif mode == "dark":
        paper = "rgba(0,0,0,.95)"
        plot_bg = "rgba(0,0,0,.95)"
        font_color = "white"

    fig.update_layout(
        paper_bgcolor=paper,
        plot_bgcolor=plot_bg,
        font_color=font_color,
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(1,0,0,0)"},
        dragmode=False,
        xaxis_title=None,
        margin={"r": 8, "t": 50, "l": 5, "b": 15},
    )
    return fig


def format_active_axes(fig, min_range=None, max_range=None, units=None):
    """ This function formats the axes of a figure. """

    if mode == "dark":
        tickcolor = "rgba(255,255,255,1)"
        gridcolor = "white"
    else:
        tickcolor = "rgba(0,0,0,1)"
        gridcolor = "black"

    fig.update_xaxes(
        showgrid=False,
        showline=True,
        ticks="outside",
        tickwidth=1,
        ticklen=7,
        tickcolor=tickcolor,
        tickfont=dict(size=14),
        linecolor=gridcolor,
    )

    if units == "Year":
        fig.update_xaxes(range=[2000, 2022])
    elif units == "SomeYears":
        fig.update_xaxes(range=[2005, 2020])
    elif units == "ForArima":
        fig.update_xaxes(range=[2005, 2022])

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
        linecolor=gridcolor,
    )

    if min_range is not None and min_range >= 0:
        fig.update_yaxes(
            range=[min_range - (min_range * 0.1), max_range + (max_range * 0.1)],
        )
    elif units == 'ForArima':

        try:
            fig.update_yaxes(
                range=[0,max_range + (max_range * .20)]
            )
        except Exception as E:
            print(E)
            
    return fig


#################################
# BLANK VISUAL
#################################


def blank():
    fig = px.scatter()
    fig = format_active_axes(fig)
    fig = format_active_layout(fig)
    text1 = 'Hmmm, this is unfortunate.<br><br> We wanted to show you something,<br>'
    text2 = 'but we are having trouble finding it right now!<br><br>'
    text3 = 'Please be patient while we search the house.'
    
    fig.add_annotation(
        dict(
            # xref="x1",
            # yref="y1",
            text=text1 + text2 + text3,
            showarrow=False,
            # ax=0,
            # ay=-40,
            font={"color": 'black', 'size': 15},
        ),
    )
    return fig


#################################
# ARIMA VISUALIZATIONS
#################################


def arima_visual_controller(df, target, params, differenced, results):

    try:
        fig = build_differencing_chart(differenced, target, results)
    except Exception as E:
        print('Differencing Error: ', E)
        fig = blank()
    
    try:
        fig2 = plot_arima_predictions(df, target, params[0])
    except Exception as E:
        print('Prediction Error: ', E)
        fig2 = blank()

    return fig, fig2


def plot_arima_predictions(df, target, locale):

    df["Year"] = df.Year.astype("int")

    df.loc[(df.Year < 2019), "full_results"] = None

    trace1 = go.Scatter(
        x=df["Year"],
        y=df["full_results"],
        name="Income Prediction",
        mode="lines+markers",
        marker_color="black",
    )

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
    fig.add_traces(trace1)
    fig.add_vrect(
        x0=2019,
        x1=2022.5,
        fillcolor="green",
        opacity=0.3,
        line_width=0,
        annotation_text="Predicted Period",
        annotation_position="left",
    )
    if df['MedianIncome'].max() >= df['full_results'].max():
        max_range = df['MedianIncome'].max()
    else:
        max_range = df['full_results'].max()
        
    fig = format_active_layout(fig)
    fig = format_active_axes(fig, max_range = max_range, units="ForArima")
    age_group = df.AgeGroup.unique().tolist()[0]

    fig.update_layout(
        showlegend=True,
        title=dict(
            text=f"ARIMA Predicted Median Income vs. Actual<br>    {locale_options[locale]} | Age Group: {age_group}",
            font=dict(size=22),
        ),
    )
    fig.update_layout(
        legend=dict(
            font_color="black", title="", orientation="h", bgcolor=("rgba(0,0,0,0)"),
        ),
    )

    return fig


def build_differencing_chart(df, target, results):

    df.index = df.index.astype("str")

    fig = make_subplots(rows=3, cols=1)

    fig.append_trace(
        go.Scatter(x=df["Year"], y=df[target], marker=dict(color="black", size=3)),
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

    fips = df.FIPS.unique().tolist()[0]
    age_group = df.AgeGroup.unique().tolist()[0]
    fig.update_layout(
        title=dict(
            text=f"Differenced Data | {locale_options[fips]} | Age Group: {age_group}",
            font=dict(size=22),
        ),
        margin={"r": 10, "t": 50, "l": 5, "b": 25},
        showlegend=False,
    )
    results_dict = results[0]
    adf_text = "Not Differenced"
    adf = round(results_dict["ADF Statistic"], 3)
    pval = round(results_dict["P-Value"], 9)
    display_string = f"{adf_text}<br>ADF Stat: {adf}<br>P-Value: {pval}"

    if pval < 0.05:
        font_col = "green"
        display_string = "<b>" + display_string + "<b>"
    else:
        font_col = "black"

    data_mean = df[target].mean()
    data_max = df[target].max()
    fig.add_annotation(
        dict(
            y=data_mean + (data_max - data_mean),
            xref="x1",
            yref="y1",
            text=display_string,
            showarrow=False,
            ax=0,
            ay=-40,
            font={"color": font_col},
        ),
    )

    results_dict = results[1]
    adf_text = "Differenced Once"
    adf = round(results_dict["ADF Statistic"], 3)
    pval = round(results_dict["P-Value"], 9)
    display_string = f"{adf_text}<br>ADF Stat: {adf}<br>P-Value: {pval}"

    if pval < 0.05:
        font_col = "green"
        display_string = "<b>" + display_string + "<b>"
    else:
        font_col = "black"

    data_mean = df["diff_1"].mean()
    data_max = df["diff_1"].max()

    fig.add_annotation(
        dict(
            y=data_mean + (data_max - data_mean),
            xref="x1",
            yref="y2",
            text=display_string,
            showarrow=False,
            ax=0,
            ay=-40,
            font={"color": font_col},
        ),
    )

    results_dict = results[2]
    adf_text = "Differenced Twice"
    adf = round(results_dict["ADF Statistic"], 3)
    pval = round(results_dict["P-Value"], 9)
    display_string = f"{adf_text}<br>ADF Stat: {adf}<br>P-Value: {pval}"

    if pval < 0.05:
        font_col = "green"
        display_string = "<b>" + display_string + "<b>"
    else:
        font_col = "black"

    data_mean = df["diff_2"].mean()
    data_max = df["diff_2"].max()

    fig.add_annotation(
        dict(
            # x=1, y=1, # annotation point
            y=data_mean + (data_max - data_mean),
            xref="x1",
            yref="y3",
            text=display_string,
            showarrow=False,
            ax=0,
            ay=-40,
            font={"color": font_col},
        ),
    )
    fig = format_active_layout(fig)

    fig = format_active_axes(fig, min_range=None, max_range=None, units="SomeYears")
    fig.update_layout()

    return fig


#################################
# ANALYSIS PAGE VISUAL CONTROLLERS
#################################


def income_visual_master(yearly_income, target_fips):

    try:
        full, df = next(yearly_income)
    except Exception as E:
        print(E)

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
    try:
        fig3 = build_average_house_prices(df, args)
    except Exception as E:
        print(E)
    return fig3


#################################
# ANALYSIS PAGE VISUAL BUILDERS
#################################


def income_by_age_group(df, args):
    color_map = map_colors()

    age_group_list = df.AgeGroup.unique().tolist()

    subset = df[(df.AgeGroup != "overall")].copy()

    # Create List of Figure

    fig = go.Figure(
        go.Scatter(
            x=df["Year"].unique(),
            y=df[(df.AgeGroup == "overall")]["MedianIncome"],
            hoveron="points+fills",
            fillcolor="lightgrey",
            name="Overall Average",
            fill="tozeroy",
            line=dict(width=2, color="rgb(0, 0, 0)"),
        )
    )

    fig1 = px.line(
        x=subset["Year"],
        y=subset["MedianIncome"],
        color=subset["AgeGroup"],
        color_discrete_map=color_map,
    )
    fig.add_traces(fig1.data)

    # Add Rectangles
    max_year = df.dropna().Year.max()
    try:
        fig.add_vrect(
            x0=2000,
            x1=2005,
            fillcolor="red",
            opacity=0.2,
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

    # Add preliminary formatting
    min_range, max_range, locale = args
    fig.update_layout(
        title=dict(
            text=f"<b>Median Income by Age Group | {locale}<b>", font=dict(size=20)
        ),
        legend=dict(
            font_color="black", title="", orientation="h", bgcolor=("rgba(0,0,0,0)"),
        ),
    )
    # Send out for final formatting
    fig = format_active_layout(fig)
    fig = format_active_axes(fig, min_range, max_range, "Year")
    return fig


def build_average_median_income(df):

    # Filter Dataset
    df = df[(df.AgeGroup != "overall")]
    df = df.groupby(by=["FIPS", "County"])[["MedianIncome"]].agg("mean").reset_index()
    df.sort_values(by="MedianIncome", ascending=True, inplace=True)
    df = df.tail(5)
    df["displayed_text"] = df["MedianIncome"].apply(
        lambda x: "$" + "{:,}".format(round(x, 2))
    )

    # Create Figure
    fig = px.bar(df, x="MedianIncome", y="County", text="displayed_text", opacity=0.7)

    # Send out for formatting.
    fig = format_active_layout(fig)
    fig = format_active_axes(fig)

    # Adjust formatting
    fig.update_yaxes(tickprefix="", title=None)
    fig.update_xaxes(showticklabels=False, ticks=None)

    # Set Title
    fig.update_layout(
        title=dict(
            text=f"<b>Counties with Highest Overall Average Median Income<b>",
            font=dict(size=20),
        )
    )

    # Add text to bars
    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        textfont={"color": "black", "size": 16},
    )
    fig.update_xaxes(showline=False)
    return fig

    fig.update_traces(line=dict(width=2))

    min_range, max_range, locale = args
    fig.update_layout(
        title=dict(
            text=f"<b>Median Income by Age Group | {locale}<b>", font=dict(size=20)
        ),
        paper_bgcolor="rgba(0,0,0,.1)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
        legend=dict(title="", orientation="h", bgcolor=("rgba(0,0,0,0)"),),
    )
    fig = format_active_layout(fig)
    fig = format_active_axes(fig, min_range, max_range, "Year")
    return fig


def build_average_house_prices(df, args):
    df = df.drop_duplicates()

    current_year = df.dropna().Year.max()
    current_price = df.dropna().MedianHousePrice.tail(1).max()
    min_price = df.dropna().MedianHousePrice.min()
    current_text_price = "${:,.0f}".format(current_price)
    current_date = df.dropna().Date.max()
    text_date = dt.datetime.strftime(
        dt.datetime.strptime(current_date, "%Y-%m-%d"), "%B %Y"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MedianHousePrice"],
            hoveron="points+fills",
            fillcolor="lightgrey",
            name="Median Income",
            fill="tozeroy",
            line=dict(width=2, color="rgb(0, 0, 0)"),
        )
    )

    min_range, max_range, locale = args

    fig.update_layout(
        title=dict(text=f"<b>Median House Price for {locale}<b>", font=dict(size=20),),
        showlegend=False,
    )

    anchor = "left" if current_year < 2007 else "right"
    xanch = 30 if current_year < 2007 else -30
    yanch = 0 if current_year < 2007 else 0
    fig.add_annotation(
        text=f"{text_date}<br>Median Price: {current_text_price}",
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=2,
        xref="x",
        yref="y",
        ayref="y domain",
        axref="pixel",
        ay=yanch,
        ax=xanch,
        x=current_date,
        y=min_price / 2,
        xanchor=anchor,
        yanchor="middle",
        align="right",
        font=dict(size=14, color="black"),
    )
    fig = format_active_layout(fig)
    fig = format_active_axes(fig, min_range, max_range, "Date")
    return fig


def build_income_vs_house_price(year_income_hp):
    # I think that if we do a baseline year in 2005, and then show a chart indicating how much each has moved
    # from that baseline, it could be a powerful visual.

    fig = px.line()
    fig.add_scatter(
        x=year_income_hp["Year"],
        y=year_income_hp["MedianHousePrice"],
        name="Median House Price",
        line_width=3,
    )
    fig.add_scatter(
        x=year_income_hp["Year"],
        y=year_income_hp["MedianIncome"],
        name="Median Income",
        line_width=3,
    )
    fig.update_layout(
        title=dict(
            text=f"<b>Median House Prices vs. Median Income<b>", font=dict(size=20),
        ),
    )
    fig = format_active_layout(fig)
    fig = format_active_axes(fig, units="Year")
    fig.update_layout(
        legend=dict(
            font_color="black",
            title="",
            orientation="h",
            # yanchor="top",
            # y=1.13,
            # xanchor="left",
            # x=0.18,
            bgcolor=("rgba(0,0,0,0)"),
        ),
    )
    return fig


#################################
# MAP VISUALIZATIONS MENU FORMATTING
#################################

def build_table_for_data(df):
    print("In the table builder")
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[_] for _ in df.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    return fig


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
        opacity=0.9,
        animation_frame=animate,
        range_color=scale,
        color_continuous_scale="Bugn",
        hover_data=["County", "MedianIncome", "AgeGroup"],
    )
    fig.update_traces(
        hovertemplate="<b>County: %{customdata[0]}</b><br>Median Income: %{customdata[1]:$,}<br>Age Group: %{customdata[2]}"
    )
    return fig


def build_affordability_map(df, base_map_style, scale, animate):

    for locale in locale_options:
        if locale not in df.FIPS.unique().tolist():
            new_row = [None, locale, None, locale_options[locale], None, None, None, None, 'Missing']
            columns = df.columns.tolist()
            new_row = zip(columns, new_row)
            new_row = {val[0]: val[1] for val in new_row}
            temp_df = pd.DataFrame(new_row, index = [1])

            df = pd.concat([df, temp_df])

    df['Year'] = df['Year'].dropna().tolist()[0]
    df['AgeGroup'] = df['AgeGroup'].dropna().tolist()[0]
    
    colors = {"Yes": "#1D9A6C", "No": "#FF1493", "Missing": "#73666D"}
    customdata = np.stack(
        (df["County"], df["MonthlyMortgage"], df["AgeGroup"]), axis=-1
    )
    try:
        fig = px.choropleth_mapbox(
            df,
            geojson=counties,
            color="affordable",
            locations="FIPS",
            featureidkey="properties.FIPSSTCO",
            center={"lat": 40.15, "lon": -74.421983},
            mapbox_style=base_map_style,
            color_discrete_map=colors,
            zoom=6.5,
            opacity=1,
            hover_data=["County", "MonthlyMortgage", "AgeGroup"],
        )
    except Exception as E:
        print(E)
    fig.update_traces(
        hovertemplate="<b>County: %{customdata[0]}</b><br>Monthly Mortgage: %{customdata[1]:$,}<br>Age Group: %{customdata[2]}"
    )
    return fig


def map_builder(
    generator,
    base_map_style,
    age_group,
    target_year,
    animate,
    args,
    target="MedianIncome",
):
    map_mode = animate
    
    if not args:
        df = next(generator)
        df = df[(df[target] > 0)]
        df = df.drop(columns=["Month", "MedianHousePrice"])

    else:
        df = generator.send(args)

    if animate == "animated":
        print("Building Animated Map")
        map_title = f"Median Income (Animated) | {age_group}"
        df = df[(df.AgeGroup == age_group)]
        scale = [df[target].min(), df[target].max()]
        df.drop_duplicates(inplace=True)
        df = df.sort_values(by="Year")
        fig = build_animated_map(df, base_map_style, scale, "Year")
        fig = format_map_menu(fig)

    elif animate == "static":
        print("Building Static Map")
        map_title = f"Median Income | {age_group} | {target_year}"
        df = df[(df.Year == target_year) & (df.AgeGroup == age_group)]
        scale = [df[target].min(), df[target].max()]
        df = df.drop_duplicates()
        fig = build_animated_map(df, base_map_style, scale, None)

        
    elif (animate == "static-affordability" or animate == 'static_table'):
        print("Building Static Affordability Map")
        map_title = f"Home Affordability | {age_group} | {target_year}"
        df = df[(df.AgeGroup == age_group) & (df.Year == target_year)]
        scale = None
        animate = "static"
        df.drop_duplicates(inplace=True)
        if (target_year > 2019 and map_mode == 'static_table'):
            df.replace([np.inf, -np.inf], np.nan, inplace = True)
            df.dropna(inplace = True)
            df = df.drop(columns = ['FIPS'])
            fig = build_table_for_data(df)
        else:
            fig = build_affordability_map(df, base_map_style, scale, animate)

    font_color='white' if base_map_style == 'carto-darkmatter' else 'black'
    fig.update_layout(
        coloraxis_showscale=True,
        title=dict(text=f"<b>{map_title}<b>", font=dict(size=28)),
        margin={"r": 0, "t": 0, "l": 0, "b": 0, "autoexpand": True},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=font_color,
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    if map_mode not in ["static-affordability", 'static_table']:
        fig.update_layout(
            title_y=0.96,
            title_x=0.05,
            # legend=dict(x=0.9, y=0.4),
            coloraxis_colorbar=dict(
                title=f"{feature_options[target]}",
                titlefont=dict(color="white", size=15),
                ticks="inside",
                ticklen=24,
                thickness=25,
                tickcolor="white",
                tickfont=dict(color="white", size=14),
                tickprefix="$",
                len=0.85,
            ),
        )

    if map_mode in ["static-affordability", 'static_table']:
        fig.update_layout(
            title_y=0.96,
            title_x=0.05,
            legend=dict(
                bordercolor="black",
                borderwidth=2,
                bgcolor="rgba(255,255,255,.7)",
                x=0.97,
                y=0.4,
                font=dict(color="black", size=16),
                xanchor="right",
                title=dict(text="Is the County Affordable?"),
            ),
        )
    if map_mode == 'static_table':
        fig.update_layout(
            title = '',
            title_text="To view the median income map again, set the year to less than 2020.",
            margin={"r": 0, "t": 45, "l": 0, "b": 0, "autoexpand": True},
        )

    return fig


#################################
# POLYNOMIAL VISUALS - DEPRECATED
#################################


# def build_polynomial_model(model_data, target, locale, best):
#     """ This function creates a visualization for a polynomial regression model. """

#     # This data was returned from a generator yield on the MODEL_LAYOUT page.
#     # It is yielded from the poly_generator in the data_control.py file
#     # It is received in a list and unpacked in the code below.
#     try:
#         i, predictions, original, futures = model_data
#     except Exception as E:
#         print("Error in build_polynomial_model", E)

#     # Get the dates for the predictions
#     freq = "M" if target != "MedianIncome" else "Y"
#     num_periods = futures.shape[0]
#     fixed_dates = data_con.get_date_range(
#         original["date"].dropna().tolist()[-1], num_periods, freq
#     )

#     # Add the prediction dates to the prediction df
#     futures["date"] = fixed_dates

#     # combine all the dataframes
#     data_for_plotting = pd.merge(
#         original, predictions, left_on="predictor", right_on="x_var", how="outer"
#     )
#     data_for_plotting = pd.merge(
#         data_for_plotting,
#         futures,
#         left_on=["predictor", "date"],
#         right_on=["predictor", "date"],
#         how="outer",
#     )
#     data_for_plotting["date"] = pd.to_datetime(data_for_plotting["date"])

#     # Create the first trace
#     if target == "MedianIncome":
#         fig1 = px.scatter(x=data_for_plotting["date"], y=data_for_plotting[target])
#         fig1.update_traces(
#             mode="markers",
#             marker_line_width=2,
#             marker_size=15,
#             marker_color="rgba(0,0,255,.3)",
#         )

#     else:
#         fig1 = px.line(x=data_for_plotting["date"], y=data_for_plotting[target])
#         fig1.update_traces(line=dict(color="black", width=3))

#     # Create the second trace
#     fig2 = px.line(x=data_for_plotting["date"], y=data_for_plotting["predictions"])

#     fig3 = px.line(x=data_for_plotting["date"], y=data_for_plotting["futures"])

#     fig2.update_traces(line=dict(color="white", width=3, dash="dash"))
#     fig3.update_traces(line=dict(color="red", width=3, dash="dash"))

#     # Combine the traces into a single figure
#     final_fig = go.Figure(data=fig1.data + fig2.data + fig3.data)

#     if best:
#         indicate_best = "| Lowest RMSE | (Animation Paused)"
#     else:
#         indicate_best = ""

#     title_string = f"""
#     <b>{feature_options[target]} | Degrees: {i}<br>
#     {locale_options[locale]} {indicate_best}<b>
#     """
#     # Add and format the title
#     final_fig.update_layout(title=dict(text=title_string, font=dict(size=20),))

#     min_range = original[target].min()
#     max_range = original[target].max()

#     # Send the figure out for formatting.
#     final_fig = format_active_layout(final_fig)

#     final_fig = format_active_axes(final_fig, min_range, max_range)
#     return final_fig


# Possible Trash
##########################################33

# def build_income_line_chart(income_df):
#     """ This function builds a filled area chart (which can be easily turned into a line chart)"""

#     fig = px.line(income_df, x="Year", y="MedianIncome", color="FIPS")

#     fig.update_layout(
#         title=dict(text="<b>Chart 4<b>", font=dict(size=20)),
#         paper_bgcolor="rgba(255,255,255,1)",
#         plot_bgcolor="rgba(255,255,255,1)",
#         font_color="white",
#         modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
#     )
#     fig.update_xaxes(ticks="outside", tickwidth=1, ticklen=7, tickcolor="rgba(0,0,0,0)")
#     fig.update_yaxes(ticks="outside", tickwidth=1, ticklen=6, tickcolor="rgba(0,0,0,0)")

#     return fig



# def build_fig_four():

#     print("\nBuilding Median Income by Age Group chart.")
#     df = data_con.income_data()

#     fig = px.bar(
#         x=df["Year"], y=df["MedianIncome"], color=df["AgeGroup"], barmode="group"
#     )
#     fig.update_layout(
#         title=dict(text="<b>Median Income by Age Group<b>", font=dict(size=20)),
#         paper_bgcolor="rgba(0,0,0,.2)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         font_color="white",
#         modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,0)"},
#     )
#     fig.update_xaxes(ticks="outside", tickwidth=1, ticklen=7, tickcolor="rgba(0,0,0,0)")
#     fig.update_yaxes(ticks="outside", tickwidth=1, ticklen=6, tickcolor="rgba(0,0,0,0)")
#     print("Finished Building Median Income by Age Group Chart\n")
#     return fig


# def build_fig_two(df, args):
#     start = time.perf_counter()
#     # df = new_data_con.income_data_generator()
#     color_map = map_colors()
#     fig = px.bar(
#         x=df["Year"],
#         y=df["MedianIncome"],
#         color=df["AgeGroup"],
#         barmode="group",
#         color_discrete_map=color_map,
#     )

#     min_range, max_range, locale = args
#     fig.update_layout(
#         title=dict(
#             text=f"<b>Median Income by Age Group for {locale}<b>", font=dict(size=20),
#         ),
#     )
#     fig = format_active_axes(fig, min_range, max_range, "Year")
#     build_time = round(time.perf_counter() - start, 3)
#     return fig, build_time


# def build_fig_one(df, args):

#     color_map = map_colors()
#     fig = px.line(
#         x=df["Year"],
#         y=df["MedianIncome"],
#         color=df["AgeGroup"],
#         color_discrete_map=color_map,
#     )

#     max_year = df.dropna().Year.max()
#     try:
#         fig.add_vrect(
#             x0=2000,
#             x1=2005,
#             fillcolor="red",
#             opacity=0.3,
#             line_width=0,
#             annotation_text="No Data",
#             annotation_position="top left",
#         )

#         fig.add_vrect(
#             x0=2019,
#             x1=2022,
#             fillcolor="red",
#             opacity=0.20,
#             line_width=0,
#             annotation_text="No Data",
#             annotation_position="top left",
#         )
#     except Exception as E:
#         print(E)


# def build_arima_visual(df, target):

#     trace1 = px.line(x=df["Year"], y=df["converted"])
#     trace2 = px.line(x=df["Year"], y=df["MedianIncome"])

#     fig = go.Figure(data=trace1.data + trace2.data)
#     fig = format_active_layout(fig)

#     fig = format_active_axes(
#         fig, min_range=False, max_range=False, units="False"
#     )
#     return fig


# def old_arima_visual_controller(arima_gen, target, locale, age_group):

#     # df, differenced_df, arima_step = arima_gen.send([target, [locale, age_group]])
#     df, arima_step = arima_gen.send([target, [locale, age_group]])

#     df["Year"] = df["Year"].astype("str")
#     df.index = df.index.astype("str")

#     fig1 = build_differencing_chart(df, target)
#     # fig2 = build_arima_visual(df, target)
#     print("Ready for fig display")
#     return fig1  # , fig2


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
