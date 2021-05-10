import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import app0,app1new,app2,app3

app.layout = html.Div(children=[
    html.H1(children='Climate Change Dashboard', style={
        'textAlign': 'center'
    }),

    html.Img(src="/assets/climate change.png", height="30px"),

    html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Top 5 Nations |', href='/apps/app0'),
        dcc.Link('Emissions Level & Demographics |', href='/apps/app1new'),
        dcc.Link('Energy Usage |', href='/apps/app2'),
        dcc.Link('Understand Correlation', href='/apps/app3')
    ], className="row"),
    html.Div(id='page-content', children=[])
])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app0':
        return app0.layout
    elif pathname == '/apps/app1new':
        return app1new.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/app3':
        return app3.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
