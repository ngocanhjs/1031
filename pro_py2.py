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
    marker=dict(color=['goldenrod','hotpink','chocolate','lawngreen','dodgerblue','darkviolet','plum','forestgreen','crimson','yellow'])
)
data_bar = [trace_bar]
layout_bar = go.Layout(
    title='Top 5 countries with the most TV shows (1970-2020)',
    xaxis=dict(title='Main Production'),
    yaxis=dict(title='Number of TV shows')
)
fig_bar = go.Figure(data=data_bar, layout=layout_bar)

# Create the box chart
fig_box = px.box(data, x="MAIN_GENRE", y="SCORE", color="MAIN_GENRE", 
                title="The box chart demonstrates the distribution of range score of TV shows according to TV show genres",
                color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), ['goldenrod','hotpink','chocolate','lawngreen','dodgerblue','darkviolet','plum','forestgreen','crimson','yellow'])})
med_score = data.groupby('MAIN_GENRE')['SCORE'].median().sort_values()
sorted_genre = med_score.index.tolist()
fig_box.update_layout(xaxis=dict(categoryorder='array', categoryarray=sorted_genre))

#Create the scatter chart
fig_scatter = px.scatter(data,x= "RELEASE_YEAR", y ="SCORE", color = 'MAIN_GENRE')
# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(
    [
        html.H1('NETFLIX TV SHOW DATA VISUALIZATION', style={'text-align': 'center'}),
        html.H6("This interactive web application includes a bar chart visualizing the top 5 countries with the highest Netflix TV show production, as well as a box chart displaying the distribution of scores within different genres. Users can interact with the slider and dropdown menu to explore the data.", style={'text-align': 'center', 'color': 'lightgray', 'font-style': 'italic'}),
        html.A('Click here for more information',href='https://www.netflix.com/', style={'text-align': 'center', 'color': '#607D8B','font-style': 'italic','font-size': '14px'}),
        html.Hr(),
        dbc.Row(
            [
                html.H2('Top Countries with Most TV Shows', style={'text-align': 'center', 'color': 'black'}),
                html.Hr(),
                html.H5('THE BAR CHART'),
                html.P('Number of countries:'),
                dcc.Slider(id='slider', min=1, max=5, step=1, value=5),
                dcc.Graph(id='plot-bar', figure=fig_bar)
            ]
        ),
        html.Hr(),
        dbc.Row(
            [ 
                html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
                dbc.Col(
                    [
                        html.Hr(),
                html.H5('THE MAIN BOX CHART', style={'text-align': 'center'}),
                        dcc.Graph(id='plot-box', figure=fig_box, style={'height': 750}),
                    ],
                    width={'size': 9, 'offset': 0, 'order': 2}
                ),
                dbc.Col(
                    [
                         html.Hr(),
                         html.H5('THE SUB BOX CHART', className='text-center'),
                         html.Hr(),
                         html.H6('Select genre that you want to see:', className='text-center'),
                        dcc.Dropdown(
                            id='dropdown',
                            options=[{"label": option, "value": option} for option in data["MAIN_GENRE"].unique()],
                            value="drama"
                        ),
                        dcc.Graph(id="plot-box")
                    ]
                ),html.Hr(),
         dbc.Row(
                [
                  html.H2('The Scatter plot',style={'text-align': 'center', 'color': 'black'}),  
                  dbc.Col(
                      [
                          html.Hr(),
                          html.H5('The main scatter plot', style={'text-align': 'center'} ),
                          dcc.Graph(id='plot-scatter', figure=fig_scatter)
                      ],
                dbc.Col(
                    [
                        html.Hr(),
                        html.H5('The sub scatter',className='text-center'),
                        html.Hr(),
                        html.H6('Select genre that you want:',className='text-center'),
                        html.Div(children=[
                        dcc.Checklist(
                            id='checkbox',
                            options= [{"label": option, "value": option} for option in data["MAIN_GENRE"].unique()],
                            value="drama"
                        ),
                        dcc.Graph(id="plot-scatter")
                ], style={'display': 'flex', 'flex-direction': 'row'}
                    ]
                )
                  )  
                  ]
              )  
            ]
        )
    ],
    fluid=True
)

# Callback to update the bar chart based on the slider value
@app.callback(Output('plot-bar', 'figure'), [Input('slider', 'value')])
def update_bar_chart(value):
    df1 = df_bar.nlargest(n=value, keep='all').sort_values(ascending=False)
    fig_bar.update_layout(title='Top {} countries that have the most TV shows in the period 1970 - 2020'.format(value))
    fig_bar.update_traces(y=df1.values, x=df1.index)
    return fig_bar

# Callback to update the box chart based on the dropdown selection
@app.callback(Output('plot-box', 'figure'), [Input('dropdown', 'value')])
def update_box_chart(genre_selection):
    data_subset = data.loc[data['MAIN_GENRE'] == genre_selection]
    fig = px.box(data_subset, x="MAIN_GENRE", y="SCORE", color="MAIN_GENRE", title=f"The chart for {genre_selection} genre",
                color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), ['goldenrod','hotpink','chocolate','lawngreen','dodgerblue','darkviolet','plum','forestgreen','crimson','yellow'])})
    return fig

#Callback to update the scatter chart based on the box checklist
@app.callback(Output('plot-scatter', 'figure'), [Input('checkbox', 'value')])
def update_box_chart(genre_selection):
    data_subset = data.loc[data['MAIN_GENRE'] == genre_selection]
    fig = px.scatter(data_subset,x= "RELEASE_YEAR", y ="SCORE", color = 'MAIN_GENRE', title=f"The chart for {genre_selection} genre",
                color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), ['goldenrod','hotpink','chocolate','lawngreen','dodgerblue','darkviolet','plum','forestgreen','crimson','yellow'])})
    return fig
# Run the app
if __name__== '__main_':
    app.run_server(debug=True)
