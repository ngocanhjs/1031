import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read the CSV data
data = pd.read_csv('https://raw.githubusercontent.com/ngocanhjs/1031/main/data.csv') 

# Generate the bar chart
df = data['MAIN_PRODUCTION'].value_counts()
value = 5
df1 = df.nlargest(n=value, keep='all').sort_values(ascending=False)
trace = go.Bar(
    x=df1.values,
    y=df1.index,
    orientation='v',
    marker=dict(color=['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue'])
)
data_bar = [trace]
layout_bar = go.Layout(
    title='Top {} countries with the most TV shows'.format(value),
    xaxis=dict(title='Number of TV Shows'),
    yaxis=dict(title='Country')
)
fig_bar = go.Figure(data=data_bar, layout=layout_bar)

# Generate the dropdown options for the genre
dropdown_options = [{"label": option, "value": option} for option in data["MAIN_GENRE"].unique()]

# Create the app and define the layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.layout = html.Div([
    html.H1('TV Show Dashboard', style={'text-align': 'center'}),
    dbc.Row([
        dbc.Col([
            html.H3('Top Countries with the Most TV Shows'),
            dcc.Graph(id='bar-chart', figure=fig_bar),
            html.P('Number of countries:'),
            dcc.Slider(id='slider', min=1, max=10, step=1, value=value)
        ]),
        dbc.Col([
            html.H3('Distribution of TV Show Scores by Genre'),
            html.Hr(),
            html.H5('Select a genre:', className='text-center'),
            dcc.Dropdown(
                id='dropdown',
                options=dropdown_options,
                value='drama'
            ),
            dcc.Graph(id='box-chart')
        ])
    ])
])


# Callback to update the bar chart based on the slider value
@app.callback(Output('bar-chart', 'figure'), [Input('slider', 'value')])
def update_bar_chart(value):
    df1 = df.nlargest(n=value, keep='all').sort_values(ascending=False)
    fig_bar = go.Figure(data=go.Bar(x=df1.values, y=df1.index, orientation='v'))
    fig_bar.update_layout(title='Top {} countries with the most TV shows'.format(value))
    return fig_bar


# Callback to update the box chart based on the dropdown selection
@app.callback(Output('box-chart', 'figure'), [Input('dropdown', 'value')])
def update_box_chart(genre_selection):
    data_subset = data.loc[data['MAIN_GENRE'] == genre_selection]
    fig_box = px.box(data_subset, x='MAIN_GENRE', y='SCORE', color='MAIN_GENRE')
    fig_box.update_layout(title='The box chart demonstrates the distribution of the range score of TV shows according to TV show genres')
    return fig_box


# Run the app
if __name__ == '_main_':
    app.run_server(debug=True)
