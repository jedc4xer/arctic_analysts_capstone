import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def build_fig_one():
    fig = px.bar(x = [1,2,3], y = ['blue','green','yellow'])
    fig.update_layout(
        title=dict(
            text='<b>Chart 1<b>',
            font=dict(
                size = 20
            )
        ),
        paper_bgcolor = 'rgba(0,0,0,.2)', 
        plot_bgcolor = 'rgba(0,0,0,0)',
        font_color = 'white',
        modebar = {
            'bgcolor': 'rgba(0,0,0,0)',
            'color':'rgba(0,0,0,1)'
        }
    )
    fig.update_xaxes(ticks="outside", tickwidth = 1, ticklen=7, tickcolor = 'rgba(0,0,0,0)')
    fig.update_yaxes(ticks="outside", tickwidth = 1, ticklen=6, tickcolor = 'rgba(0,0,0,0)')
    return fig

def build_fig_two():
    fig = px.bar()
    fig.update_layout(
        title=dict(
            text='<b>Chart 2<b>',
            font=dict(
                size = 20
            )
        ),
        paper_bgcolor = 'rgba(0,0,0,.1)', 
        plot_bgcolor = 'rgba(0,0,0,0)',
        font_color = 'white',
        modebar = {
            'bgcolor': 'rgba(0,0,0,0)',
            'color':'rgba(0,0,0,1)'
        }
    )
    return fig

def build_fig_three():
    fig = px.bar()
    fig.update_layout(
        title=dict(
            text='<b>Chart 3<b>',
            font=dict(
                size = 20
            )
        ),
        paper_bgcolor = 'rgba(0,0,0,.5)', 
        plot_bgcolor = 'rgba(0,0,0,0)',
        font_color = 'white',
        modebar = {
            'bgcolor': 'rgba(0,0,0,0)',
            'color':'rgba(0,0,0,1)'
        }
    )
    return fig

def build_fig_four():
    fig = px.bar()
    fig.update_layout(
        title=dict(
            text='<b>Chart 1<b>',
            font=dict(
                size = 20
            )
        ),
        paper_bgcolor = 'rgba(0,0,0,0)', 
        plot_bgcolor = 'rgba(0,0,0,0)',
        font_color = 'white',
        modebar = {
            'bgcolor': 'rgba(0,0,0,0)',
            'color':'rgba(0,0,0,1)'
        }
    )
    return fig