import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import pathlib
from pathlib import Path


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
from app import app

# get relative data folder
PATH = Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df_flat = pd.read_csv(DATA_PATH.joinpath('Dashboard_file preprocessed df.csv'))
# Here the code to preprocess the dataframe can be added. For this notebook preprocessing is done in the previous steps.


available_indicators = df_flat['Series Name'].unique()

# This code will create
layout = html.Div(children=[
    html.H1(children='Climate Change Dashboard', style={
        'textAlign': 'center', 'fontSize': 36}), html.Div(children='''How do Emissions level, Demographic information, Energy
        usage correlate to each other''', style={'textAlign': 'center', 'fontSize': 24}),

    html.Div(children='''
      Select parameters for Scatter Plot from the Dropdown. On the Left is the x-axis parameter and on the right is y -axis
      parameter. Parameters include emissions level (CO2, greenhouse gases, etc.), demographic information(Population, 
      Land Area, etc.), energy(consumption, production, investment, etc.) for the parameters selected. On the bottom is the
      year slider from 1960-Present. Each Point on the Scatter Plot denote the country and time series graph updates as the 
      points are hovered over. 
      Please note: Not all parameters will have value in each year. ''')
    ,

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators], clearable=False,
                value='Fossil fuel energy consumption (% of total)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators], clearable=False,
                value='CO2 emissions (kt)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df_flat['Year'].min(),
        max=df_flat['Year'].max(),
        value=df_flat['Year'].min(),
        marks={str(year): {'label': str(year), 'style': {'color': 'Blue', 'fontSize': 9, 'font-family': 'sans-serif'}}
               for year in df_flat['Year'].unique()}, included=False,
        step=None
    ), style={'width': '100%', 'padding': '20px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df_flat[df_flat['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Series Name'] == xaxis_column_name]['value'],
                     y=dff[dff['Series Name'] == yaxis_column_name]['value'],
                     hover_name=dff[dff['Series Name'] == yaxis_column_name]['Country Name'])

    fig.update_traces(customdata=dff[dff['Series Name'] == yaxis_column_name]['Country Name'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(dff, axis_type, title):
    fig = px.scatter(dff, x='Year', y='value')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df_flat[df_flat['Country Name'] == country_name]
    dff = dff[dff['Series Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df_flat[df_flat['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Series Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)
