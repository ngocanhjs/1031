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
    y=df_bar.values,
    x=df_bar.index,
    orientation='v',
    marker=dict(color=['goldenrod','hotpink','chocolate','lawngreen','dodgerblue'])
)
data_bar = [trace_bar]
layout_bar = go.Layout(
    title='Top 5 countries with the most TV shows (1970-2020)',
    xaxis=dict(title='Main Production'),
    yaxis=dict(title='Number of TV shows')
)
fig_bar = go.Figure(data=data_bar, layout=layout_bar)

# Create the box chart
fig_box = px.box(
    data,
    x="MAIN_GENRE",
    y="SCORE",
    color="MAIN_GENRE",
    title="The box chart demonstrates the distribution of range score of TV shows according to TV show genres"
)
med_score = data.groupby('MAIN_GENRE')['SCORE'].median().sort_values()
sorted_genre = med_score.index.tolist()
fig_box.update_layout(xaxis=dict(categoryorder='array', categoryarray=sorted_genre))

# Create the new pie chart
genre_df = data['MAIN_GENRE'].value_counts().reset_index()
genre_df = genre_df[genre_df['MAIN_GENRE'] / genre_df['MAIN_GENRE'].sum() > 0.01]
fig_pie = px.pie(
    genre_df,
    values='MAIN_GENRE',
    names='index',
    color_discrete_sequence=px.colors.sequential.RdBu
)
fig_pie.update_traces(
    textposition='inside',
    textinfo='percent+label',
    marker = dict(line = dict(color = 'white', width = 1))
)

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    
    html.H1('NETFLIX TV SHOW DATA VISUALIZATION', style={'text-align': 'center'}),
    
    html.H6("This interactive web application includes a bar chart visualizing the top 5 countries with the highest Netflix TV show production, a pie chart of country distribution, as well as a box chart displaying the distribution of scores within different genres. Users can interact with the slider and dropdown menu to explore the data.", style={'text-align': 'center', 'color': 'black', 'font-style': 'italic'}),
    
    html.A('Click here for more information', href='https://www.netflix.com/', style={'text-align': 'center', 'color': 'blue','font-style': 'italic','font-size': '14px'}),
    
    html.Hr(),

    dbc.Row([
        # Bar chart section
        html.Div([
            html.H2('Top Countries with Most TV Shows', style={'text-align': 'center', 'color': 'black'}),
            html.Hr(),
            html.H5('THE BAR CHART'),
            html.P('Number of countries:'),
            
            dcc.Slider(
                id='slider',
                min=1,
                max=5,
                step=1,
                value=5
            ),
            
            dcc.Graph(id='plot-bar', figure=fig_bar),
            
            html.H5('Dropdown', style={'text-align': 'center'}),
            
            dcc.Dropdown(
                id='dropdown',
                options=[{"label": option, "value": option} for option in data["MAIN_GENRE"].unique()],
                value="drama"
            ),

        ], className="col-md-6"),
        
        # Pie chart section
        html.Div([
            html.H2('Genre Distribution', style={'text-align': 'center', 'color': 'black'}),
            html.Hr(),
            html.H5('THE PIE CHART'),
            dcc.Graph(id='plot-pie', figure=fig_pie)
        ], className="col-md-6")

    ], style={'margin': '30px'}),
    
    html.Hr(),

    dbc.Row([
        html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
        dbc.Col([
            html.Hr(),
            html.H5('THE BOX CHART', style={'text-align': 'center'}),
            dcc.Graph(id='plot-box', figure=fig_box, style={'height': 750}),
        ], width=12,),
    ],style={'margin': '30px'}),
    
], fluid=True)

# Callback to update the bar chart based on the slider value
@app.callback(Output('plot-bar', 'figure'), [Input('slider', 'value')])
def update_bar_chart(value):
    df1 = df_bar.nlargest(n=value, keep='all').sort_values(ascending=False)
    fig_bar.update_layout(title='Top {} countries that have the most TV shows in the period 1970 - 2020'.format(value))
    fig_bar.update_traces(y=df1.values, x=df1.index)
    return fig_bar

if __name__ == '_main_':
    app.run_server(debug=False)
