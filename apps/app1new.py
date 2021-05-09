import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df_flat = pd.read_csv(DATA_PATH.joinpath('Dashboard_file preprocessed df.csv'))
# Here the code to preprocess the dataframe can be added. For this notebook preprocessing is done in the previous steps.


available_country = df_flat['Country Name'].unique()

# Below code defines the layout of the dashboard. It defines how the dashboard will appear as a web page.
# For this dashboard, there are two dropdowns to select two countries for comparison and eight time series chart for the
# pre-defined parameters which get updated based on the country selected.

# Dash Core Component - Dropdown and Graph is being used where Time-series graph will update based on country selected

app.layout = html.Div(children=[
    html.H1(children='Climate Change Dashboard', style={
        'textAlign': 'center', 'fontSize': 36}),
    html.Div(children='''How do countries around the world compare for Greenhouse Gases emissions, Population 
                                         and GDP''', style={'textAlign': 'center', 'fontSize': 24})
    ,
    html.Div(children='''
      Select two countries for comparative trend analysis across the years''', style={
        'textAlign': 'center'})
    ,

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country1',
                options=[{'label': i, 'value': i} for i in available_country],
                value='United States', clearable=False
            )], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='country2',
                options=[{'label': i, 'value': i} for i in available_country],
                value='China', clearable=False
            )], style={'width': '49%', 'display': 'inline-block'})],
        style={'borderBottom': 'thin lightgrey solid',
               'backgroundColor': 'rgb(250, 250, 250)',
               'padding': '10px 5px'}),
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series1')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series1')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        ),

        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series3')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series3')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series4')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series4')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series5')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series5')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series6')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series6')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series7')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series7')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        ),
    ])
])


# Below code defines the callback in the dashboard, callbacks add the interactivity in dashboard,
# Input value is from the dropdown and output is the time series chart
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'), dash.dependencies.Output('y-time-series', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
# Below code defines the function that will create a dataframe and a time series graph based on country selected in the dropdown.

def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name'] == 'CO2 emissions (kt)']
    maxv = max(CO2_df['value'])
    minv = min(CO2_df['value'])

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name'] == 'CO2 emissions (kt)']

    maxv2 = max(CO2_df2['value'])
    minv2 = min(CO2_df2['value'])

    maxva = max(maxv, maxv2)
    minva = min(minv, minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='CO2 emissions (kt)', range_y=[minva, maxva])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='CO2 emissions (kt)', range_y=[minva, maxva])
    return figure1, figure2


@app.callback(
    dash.dependencies.Output('x-time-series1', 'figure'), dash.dependencies.Output('y-time-series1', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
##Different code to find min,max values
def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name'] == 'Methane emissions (kt of CO2 equivalent)']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name'] == 'Methane emissions (kt of CO2 equivalent)']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='Methane emissions (kt of CO2 equivalent)',
                      range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='Methane emissions (kt of CO2 equivalent)',
                      range_y=[minva2, maxva2])
    return figure1, figure2


@app.callback(
    dash.dependencies.Output('x-time-series3', 'figure'), dash.dependencies.Output('y-time-series3', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name'] == 'Total greenhouse gas emissions (kt of CO2 equivalent)']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name'] == 'Total greenhouse gas emissions (kt of CO2 equivalent)']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='Total greenhouse gas emissions (kt of CO2 equivalent)',
                      range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='Total greenhouse gas emissions (kt of CO2 equivalent)',
                      range_y=[minva2, maxva2])
    return figure1, figure2


@app.callback(
    dash.dependencies.Output('x-time-series4', 'figure'), dash.dependencies.Output('y-time-series4', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name'] == 'GDP (current US$)']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name'] == 'GDP (current US$)']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='GDP (current US$)', range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='GDP (current US$)', range_y=[minva2, maxva2])
    return figure1, figure2


@app.callback(
    dash.dependencies.Output('x-time-series5', 'figure'), dash.dependencies.Output('y-time-series5', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name'] == 'GDP growth (annual %)']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name'] == 'GDP growth (annual %)']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='GDP growth (annual %)', range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='GDP growth (annual %)', range_y=[minva2, maxva2])
    return figure1, figure2


@app.callback(
    dash.dependencies.Output('x-time-series7', 'figure'), dash.dependencies.Output('y-time-series7', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name'] == 'Population growth (annual %)']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name'] == 'Population growth (annual %)']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='Population growth (annual %)', range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='Population growth (annual %)', range_y=[minva2, maxva2])
    return figure1, figure2


@app.callback(
    dash.dependencies.Output('x-time-series6', 'figure'), dash.dependencies.Output('y-time-series6', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name'] == 'Population, total']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name'] == 'Population, total']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='Population, total', range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='Population, total', range_y=[minva2, maxva2])
    return figure1, figure2
