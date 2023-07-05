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



# Create the bar chart
df_bar = data['MAIN_PRODUCTION'].value_counts().nlargest(n=5, keep='all').sort_values(ascending=False)
trace_bar = go.Bar(
    x=df_bar.values,
    y=df_bar.index,
    orientation='v',
    marker=dict(color=['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue'])
)
data_bar = [trace_bar]
layout_bar = go.Layout(
    title='Top 5 countries with the most TV shows (1970-2020)',
    xaxis=dict(title='Main Production'),
    yaxis=dict(title='Number of TV shows')
)
fig_bar = go.Figure(data=data_bar, layout=layout_bar)

# Create the box chart
fig_box = px.box(data, x="MAIN_GENRE", y="SCORE", color="MAIN_GENRE", title="Range score distribution by TV show genre")

# Create the Dash app
app = dash.Dash(__name__)
server=app.server
app.layout = dbc.Container(
    [
        html.H1("Python Project 2", className="text-center"),  # Added heading here
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H1('Top Countries with Most TV Shows', className='text-center'),
                            dcc.Graph(id='plot-bar', figure=fig_bar)
                        ]
                    ),
                    width={'size': 6, 'order': 1}
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H1('Score Distribution by Genre', className='text-center'),
                            dcc.Graph(id='plot-box', figure=fig_box)
                        ]
                    ),
                    width={'size': 6, 'order': 2}
                )
            ]
        ),
    ],
    fluid=True
)

if __name__ == '_main_':
    app.run_server(debug=True)
