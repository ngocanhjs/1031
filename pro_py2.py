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

# Create the bar charts 
df_bar = data['MAIN_PRODUCTION'].value_counts().nlargest(n=5, keep='all').sort_values(ascending=False) 
slice1 = df_bar[0:2] 
slice2 = df_bar[2:4] 
slice3 = df_bar[4:6] 
fig_1 = px.histogram(data.loc[data['MAIN_PRODUCTION'].isin(slice1.index)], x='SCORE', color='MAIN_PRODUCTION', nbins=20) 
fig_2 = px.histogram(data.loc[data['MAIN_PRODUCTION'].isin(slice2.index)], x='SCORE', color='MAIN_PRODUCTION', nbins=20) 
fig_3 = px.histogram(data.loc[data['MAIN_PRODUCTION'].isin(slice3.index)], x='SCORE', color='MAIN_PRODUCTION', nbins=20) 

# Create the box chart 
fig_box = px.box(data, x="MAIN_GENRE", y="SCORE", color="MAIN_GENRE", title="The box chart demonstrates the distribution of range score of TV shows according to TV show genres", color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), ['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue', 'darkviolet', 'plum', 'forestgreen', 'crimson', 'yellow'])}) 
med_score = data.groupby('MAIN_GENRE')['SCORE'].median().sort_values() 
sorted_genre = med_score.index.tolist() 
fig_box.update_layout(xaxis=dict(categoryorder='array', categoryarray=sorted_genre)) 

# Create the pie chart 
country_df = data['MAIN_PRODUCTION'].value_counts().reset_index() 
country_df = country_df[country_df['MAIN_PRODUCTION'] / country_df['MAIN_PRODUCTION'].sum() > 0.01] 
fig_pie = px.pie(country_df, values='MAIN_PRODUCTION', names='index', color_discrete_sequence=px.colors.sequential.RdBu) 
fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='white', width=1))) 
fig_pie.update_layout(height=400) 

# Create the scatter plot 
fig_scatter = px.scatter(data, x="RELEASE_YEAR", y="SCORE", color="MAIN_GENRE", title="The scatter plot shows the scores of TV shows by genre", color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), ['goldenrod','hotpink','chocolate', 'lawngreen','dodgerblue'])})

# Create the Dash app 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) 
server = app.server 
app.layout = dbc.Container([
    html.H1('NETFLIX TV SHOW DATA VISUALIZATION', style={'text-align': 'center'}),
    html.H6("This interactive web application includes a bar chart visualizing the top 5 countries with the highest Netflix TV show production, as well as a box chart displaying the distribution of scores within different genres. Users can interact with the slider and dropdown menu to explore the data.", style={'text-align': 'center', 'color': 'lightgray', 'font-style': 'italic'}),
    html.A('Click here for more information', href='https://www.netflix.com/', style={'text-align': 'center', 'color': '#607D8B', 'font-style': 'italic', 'font-size': '14px'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H5('THE BAR CHART'),
            html.P('Number of countries:'),
            dcc.Slider(id='slider', min=1, max=5, step=1, value=5),
            dcc.Graph(id='plot-bar', figure=fig_1)
        ], md=3),
        dbc.Col([
            dcc.Graph(id='plot-bar', figure=fig_2)
        ], md=3),
        dbc.Col([
            dcc.Graph(id='plot-bar', figure=fig_3)
        ], md=3),
        dbc.Col([
            html.H5('THE PIE CHART'),
            dcc.Graph(id='plot-pie', figure=fig_pie)
        ], md=3) 
    ]),
    html.Hr(),
    dbc.Row([
        html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
        dbc.Col([
            html.Hr(),
            html.H5('THE MAIN BOX CHART', style={'text-align': 'center'}),
            dcc.Graph(id='plot-box', figure=fig_box, style={'height': 750}),
        ], width=9),
        dbc.Col([
            html.Hr(),
            html.H5('THE SCATTER PLOT', className='text-center'),
            html.Hr(),
            html.H6('Select genre that you want to see:', className='text-center'),
            dcc.Dropdown(
                id='dropdown',
                options=[{"label": option, "value": option} for option in data["MAIN_GENRE"].unique()],
                value="drama"
            ),
            dcc.Graph(id="plot-sub-box"),
        ], width=3)
    ]) 
], fluid=True)

# Callback to update the bar chart based on the slider value 
@app.callback(Output('plot-bar', 'figure'), [Input('slider', 'value')])
def update_bar_chart(value):
    df1 = df_bar.nlargest(n=value, keep='all').sort_values(ascending=False)
    fig_1 = px.histogram(data.loc[data['MAIN_PRODUCTION'].isin(df_bar.iloc[:2].index)], x='SCORE', color='MAIN_PRODUCTION', nbins=20)
    fig_2 = px.histogram(data.loc[data['MAIN_PRODUCTION'].isin(df_bar.iloc[2:4].index)], x='SCORE', color='MAIN_PRODUCTION', nbins=20)
    fig_3 = px.histogram(data.loc[data['MAIN_PRODUCTION'].isin(df_bar.iloc[4:6].index)], x='SCORE', color='MAIN_PRODUCTION', nbins=20)
    fig_1.update_layout(title='Top 2 countries that have the most TV shows in the period 1970 - 2020')
    fig_2.update_layout(title='3rd and 4th countries that have the most TV shows in the period 1970 - 2020')
    fig_3.update_layout(title='5th and 6th countries that have the most TV shows in the period 1970 - 2020')
    return fig_1, fig_2, fig_3

# Callback to update the scatter plot based on the dropdown selection 
@app.callback(Output('plot-sub-box', 'figure'), [Input('dropdown', 'value')])
def update_scatter_plot(genre_selection):
    data_subset = data.loc[data['MAIN_GENRE'] == genre_selection]
    fig = px.scatter(data_subset, x="RELEASE_YEAR", y="SCORE", color="MAIN_GENRE", title=f"The scatter plot for {genre_selection} genre", color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), ['goldenrod','hotpink','chocolate', 'lawngreen','dodgerblue'])})
    return fig

if __name__ == '_main_':
    app.run_server(debug=True)
