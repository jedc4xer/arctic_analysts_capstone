import json
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def build_fig_one():
    fig = px.bar(x=[1, 2, 3], y=["blue", "green", "yellow"])
    fig.update_layout(
        title=dict(text="<b>Chart 1<b>", font=dict(size=20)),
        paper_bgcolor="rgba(0,0,0,.2)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    fig.update_xaxes(ticks="outside", tickwidth=1, ticklen=7, tickcolor="rgba(0,0,0,0)")
    fig.update_yaxes(ticks="outside", tickwidth=1, ticklen=6, tickcolor="rgba(0,0,0,0)")
    return fig


def build_fig_two():
    fig = px.bar()
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


def build_fig_four(house_prices):

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=house_prices["timestamp"],
            y=house_prices["record_count"],
            fill="tonexty",
            fillcolor="darkblue",
            line_color="darkblue",
        )
    )

    fig.update_layout(
        title=dict(text="<b>Chart 4<b>", font=dict(size=20)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    fig.update_xaxes(ticks="outside", tickwidth=1, ticklen=7, tickcolor="rgba(0,0,0,0)")
    fig.update_yaxes(ticks="outside", tickwidth=1, ticklen=6, tickcolor="rgba(0,0,0,0)")

    return fig

print("Loading the counties AGAIN...Need to move this to it's own file.")
with open('2021_US_Counties_3.7.json') as file:
    counties = json.load(file)
    
    
def build_map_one(df):
    data_date = df['Date'].unique().tolist()[0]
    data_date = dt.datetime.strftime(data_date, "%B %Y")
    fig = px.choropleth(
        df, 
        geojson=counties, 
        locations = 'FIPS', 
        color = 'NewUnits',
        color_continuous_scale = "rdylgn_r", 
        scope = "usa"
    )
    
    fig.update_layout(
        title=dict(
            text=f"<b>{data_date}<b>", 
            font=dict(
                size=20)
        ),
        margin={"r":5,"t":10,"l":5,"b": 5},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        modebar={"bgcolor": "rgba(0,0,0,0)", "color": "rgba(0,0,0,1)"},
    )
    fig.update_layout(
        title_y = 0.95, 
        title_x = 0.25,
        title_font_size = 18,
        legend = dict(x=0.9,y=0.6)
    )
    
    fig.update_geos(
        bgcolor='rgba(0,0,0,0)',
        resolution=50,
        landcolor='lightgrey',
        subunitcolor='black',
        showlakes=True,
        lakecolor="Blue",
        showrivers=True,
        rivercolor="Blue"
    )
    return fig