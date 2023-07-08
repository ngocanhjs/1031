import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Load the data for each chart
bar_data = pd.read_csv('https://raw.githubusercontent.com/ngocanhjs/lancuoi/main/data.csv')
box_data = pd.read_csv('C:\data.csv')
scatter_data = pd.read_csv('tv_show_data.csv')

# Create the layout for the combined charts
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[
        html.H1('Combined Charts', style={'text-align': 'center'}),
        
        html.Div(
            children=[
                html.Div(
                    dcc.Graph(id='bar-chart', figure=bar_fig),
                    style={'width': '33%', 'display': 'inline-block'}
                ),
    
                html.Div(
                    dcc.Graph(id='box-chart', figure=box_fig),
                    style={'width': '33%', 'display': 'inline-block'}
                ),
    
                html.Div(
                    dcc.Graph(id='scatter-plot', figure=scatter_fig),
                    style={'width': '33%', 'display': 'inline-block'}
                )
            ]
        )
    ]
)

# Define the callbacks to update the charts
@app.callback(
    Output('bar-chart', 'figure'),
    Input('slider', 'value')
)
def update_bar_chart(value):
    df = bar_data['MAIN_PRODUCTION'].value_counts()
    df1 = df.nlargest(n=value, keep='all').sort_values(ascending=False)
    
    trace = go.Bar(
        x=df1.values,
        y=df1.index,
        orientation='v',
        marker=dict(color=['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue', 'darkviolet', 'plum', 'forestgreen', 'crimson', 'yellow'])
    )

    data = [trace]

    layout = go.Layout(
        title='Top {} countries that have the most TV shows in the period 1970 - 2020'.format(value),
        xaxis=dict(title='MAIN_PRODUCTION'),
        yaxis=dict(title="NUMBER OF TV SHOWS")
    )

    fig = go.Figure(data=data, layout=layout)
    
    return fig


@app.callback(
    Output('box-chart', 'figure'),
    Input('dropdown', 'value')
)
def update_box_chart(genre_selection):
    data_subset = box_data.loc[box_data["MAIN_GENRE"] == genre_selection]
    fig = px.box(data_subset, x="MAIN_GENRE", y="SCORE", color="MAIN_GENRE", title=f"The chart for {genre_selection} genre")
    return fig


@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('checkbox', 'value'), Input('year_slider', 'value')]
)
def update_scatter_plot(genre_selection, year_range):
    data_subset = scatter_data.loc[(scatter_data['MAIN_GENRE'].isin(genre_selection)) & (scatter_data['RELEASE_YEAR'].isin(range(year_range[0], year_range[1] + 1)))]
    fig = px.scatter(data_subset, x="RELEASE_YEAR", y="SCORE", color="MAIN_GENRE", title="The scatter plot shows the scores of TV shows by year and genre",
                     color_discrete_map={genre: color for genre, color in zip(scatter_data['MAIN_GENRE'].unique(), ['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue', 'darkviolet', 'plum', 'forestgreen', 'crimson', 'yellow'])})
    return fig

# Run the app
if __name__ == '_main_':
    app.run_server(debug=True)
