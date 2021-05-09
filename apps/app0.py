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



CO2_df = df_flat.loc[df_flat['Series Name'] == 'CO2 emissions (kt)']
CO2_df2020 = CO2_df.loc[CO2_df['Year'] == 2016]
top5 = CO2_df2020.sort_values(by=['value'], ascending=False).head(5)
fig = px.bar(top5.sort_values(by=['value']), x='Country Name', y='value',
             labels={'value': 'CO2 emissions (kt)'}, title='CO2 emissions (kt) - Top 5 nations in Year 2016')
fig.update_xaxes(fixedrange=True)

gdp_df = df_flat.loc[df_flat['Series Name'] == 'GDP (current US$)']
gdp_df2 = gdp_df.loc[gdp_df['Year'] == 2016]
top52 = gdp_df2.sort_values(by=['value'], ascending=False).head(5)
fig2 = px.bar(top52.sort_values(by=['value']), x='Country Name', y='value',
              labels={'value': 'GDP (current US$)'}, title='GDP (current US$) - Top 5 nations in 2016')
fig2.update_xaxes(fixedrange=True)

# Below code defines the layout of the dashboard. It defines how the dashboard will appear as a web page.
app.layout = html.Div(children=[
    html.H1(children='Climate Change Dashboard', style={
        'textAlign': 'center'
    }),
    html.Div(children=''' Top 5 nations for
      CO2 emissions (kt)and GDP (current US$)''', style={
        'textAlign': 'center'
    }),
    html.Div([
                html.Div([dcc.Graph(id='bar-chart1', figure=fig)], style={'width': '49%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='bar-chart2', figure=fig2)], style={'width': '49%', 'display': 'inline-block'})
            ])
])
