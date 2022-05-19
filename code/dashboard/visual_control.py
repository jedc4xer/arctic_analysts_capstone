import json
import time
import functools
import datetime as dt
from config import counties
import plotly.express as px
import data_control as data_con
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Visual Formatting Functions
##################################

def format_active_graph_visual(fig, min_range, max_range):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,.1)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            modebar={
                "bgcolor": "rgba(0,0,0,0)", 
                "color": "rgba(1,0,0,0)"
            }
    )
    
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        ticks="outside", 
        tickwidth=1, 
        ticklen=7,
        tickcolor="rgba(255,255,255,1)"
    )
    fig.update_yaxes(
        showgrid=False, 
        showline=True, 
        range = [
            min_range - (min_range*.1),
            max_range+(min_range*.1)
        ], 
        ticks="outside", 
        tickwidth=1,
        ticklen=6, 
        tickcolor="rgba(255,255,255,1)"
    )
    return fig


# Build Model Visualizations
####################################


def build_polynomial_model(model_data, target):
    """ This function creates a visualization for a polynomial regression model. """
        
    # This data was returned from a generator yield on the MODEL_LAYOUT page.
    i, predictions, original = model_data
    
    # These were needed for the Median Income, but possibly not for the others.
    # original['predictor'] = original['predictor'].astype('int')
    # original[target] = original[target].astype('float')
    
    # Create the first trace
    fig1 = px.line(
        x = original['predictor'],
        y = original[target]
    )
    
    # Create the second trace
    fig2 = px.line(
        x=predictions['x_var'],
        y=predictions['predictions']
    )
    
    fig1.update_traces(line=dict(color='black', width=3))
    fig2.update_traces(line=dict(color='white', width=3, dash='dash'))

    # Combine the traces into a single figure
    final_fig = go.Figure(data = fig1.data + fig2.data)
    
    # Add and format the title
    final_fig.update_layout(
        title=dict(
            text=f'<b>{target} | Degrees: {i}<b>',
            font=dict(size=20),
        )
    )

    min_range = original[target].min() 
    max_range = original[target].max()

    # Send the figure out for formatting.
    final_fig = format_active_graph_visual(
        final_fig, min_range, max_range
    )
    return final_fig



def income_visual_builder(yearly_income):
    full_df = next(yearly_income)
    
    pass
def build_fig_one(yearly_income, target_fips = '34001'):
    start = time.perf_counter()
    full, df = next(yearly_income)
    min_range = 0
    max_range = full[(full.FIPS == target_fips)]['MedianIncome'].max()
    full = None
    # Filter by a county
    df = df[(df.FIPS == target_fips)]
    fig = px.bar(x=df["Year"], y=df["MedianIncome"], color=df["AgeGroup"], barmode="group")
    fig.update_layout(
        title=dict(
            text=f"<b>Median Income by Age Group for {df.FIPS.tolist()[0]}<b>",
            font=dict(size=20),
        ),
    )
    fig = format_active_graph_visual(fig, min_range, max_range)
    print(f'{round(time.perf_counter() - start,3)} seconds to build fig_one')
    return fig


def build_fig_two():
    fig = px.line()
    fig.update_layout(
        title=dict(text="<b>Chart 2<b>", font=dict(size=20)),
        paper_bgcolor="rgba(0,0,0,.1)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    return fig


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


def build_static_map_one():

    df = data_con.age_filtered_data()
    df = df[(df.date == '2022-01-15')]
    print("Building Median Home Price Choropleth Map")

    # fig = px.choropleth_mapbox(df,
    #                            geojson=counties,
    #                            color="MedianHousePrice",
    #                            locations="FIPS",
    #                            featureidkey="properties.FIPSSTCO",
    #                            center={'lat': 40.301284, 'lon': -74.421983},
    #                            mapbox_style="carto-positron",
    #                            zoom=7,
    #                           animation_frame="Year"
    #                           )

    fig = px.choropleth(
        df,
        geojson=counties,
        color="MedianHousePrice",
        locations="FIPS",
        featureidkey="properties.FIPSSTCO",
        #animation_frame="date",
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="rgba(0,0,0,0)",
        resolution=50,
        landcolor="lightgrey",
        subunitcolor="black",
    )

    fig.update_layout(
        coloraxis_showscale=False,
        title=dict(text=f"<b>{'Median Home Prices'}<b>", font=dict(size=20)),
        margin={"r": 0, "t": 0, "l": 0, "b": 0, "autoexpand": True},
        # height=1200,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    fig.update_layout(
        title_y=1, title_x=0.25, title_font_size=18, legend=dict(x=0.9, y=0.4)
    )

    print("Finished Building Median Home Price Choropleth Map")
    return fig

@functools.lru_cache()
def build_static_map_two():

    df = data_con.income_data()
    df = df.sort_values(by="Year")
    df = df[(df.Year == 2019)]
    print("Building Median Income Choropleth Map")

    fig = px.choropleth_mapbox(
        df,
        geojson=counties,
        color="MedianIncome",
        locations="FIPS",
        featureidkey="properties.FIPSSTCO",
        center={"lat": 40.15, "lon": -74.421983},
        mapbox_style="carto-positron",
        zoom=6.5,
        #animation_frame="Year",
    )

    #     fig = px.choropleth(df,
    #                        geojson=counties,
    #                        color="MedianHousePrice",
    #                         locations="FIPS",
    #                         featureidkey="properties.FIPSSTCO",
    #                         animation_frame="date"
    #                        )

    #     fig.update_geos(fitbounds="locations",
    #                     visible=False,
    #                    bgcolor="rgba(0,0,0,0)",
    #                     resolution=50,
    #                     landcolor="lightgrey",
    #                     subunitcolor="black",
    #                    )

    fig.update_layout(
        coloraxis_showscale=False,
        title=dict(text=f"<b>{'Median Income'}<b>", font=dict(size=20)),
        margin={"r": 0, "t": 0, "l": 0, "b": 0, "autoexpand": True},
        # height=1200,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="black",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    fig.update_layout(
        title_y=1, title_x=0.25, title_font_size=18, legend=dict(x=0.9, y=0.4)
    )

    print("Finished Building Median Income Choropleth Map")
    return fig
