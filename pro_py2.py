import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#Load the data
data = pd.read_csv("https://raw.githubusercontent.com/CorazonSilver/web-apps/main/netflix_titles_updated.csv")

# Create the figure for the bar chart
fig_bar = px.histogram(data, x='country', title='Number of TV Shows in Each Country', color='country', color_discrete_sequence=px.colors.qualitative.Alphabet)

# Configure the figure layout for the bar chart
fig_bar.update_layout(
    xaxis_title="Country",
    yaxis_title="Number of TV shows",
    margin=dict(l=50, r=50, t=50, b=50),
    paper_bgcolor="white"
)

# Create the figure for the box chart
fig_box = px.box(data, x='MAIN_GENRE', y='IMDB_RATING', title='Distribution of IMDb Ratings Across Genres')

# Configure the figure layout for the box chart
fig_box.update_layout(
    xaxis_title="Genre",
    yaxis_title="IMDb Rating",
    margin=dict(l=50, r=50, t=50, b=50),
    paper_bgcolor="white"
)

# Create the figure for the scatter plot
fig_scatter = px.scatter(
    data,
    x='IMDB_RATING',
    y='RELEASE_YEAR',
    color="MAIN_GENRE",
    title='IMDb Ratings vs Release Year by Genre'
)

# Configure the figure layout for the scatter plot
fig_scatter.update_layout(
    xaxis_title="IMDb Rating",
    yaxis_title="Release Year",
    margin=dict(l=50, r=50, t=50, b=50),
    paper_bgcolor="white"
)

# Create the app and apply Bootstrap CSS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the app layout
app.layout = dbc.Container(
    [
        html.Div(
            [
                html.H1('NETFLIX TV SHOW DATA VISUALIZATION', style={'text-align': 'center'}),
                html.H6("This interactive web application includes a bar chart visualizing the top 5 countries with the highest Netflix TV show production, as well as a box chart displaying the distribution of scores within different genres. Users can interact with the slider and dropdown menu to explore the data.", style={'text-align': 'center', 'color': 'lightblack', 'font-style': 'italic'}),
                html.A('Click here for more information', href='https://www.netflix.com/', style={'text-align': 'center', 'color': '#607D8B','font-style': 'italic','font-size': '14px'}),
                html.Hr(),
            ]
        ),
        dbc.Row(
            [
                html.H2('Top Countries with Most TV Shows', style={'text-align': 'center', 'color': 'black'}),
            ]
        ),
        html.Div(
            [
                dcc.Graph(id='plot-bar', figure=fig_bar),
                html.P('Number of countries:', style={'text-align': 'center'}),
                dcc.Slider(id='slider', min=1, max=5, step=1, value=5),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                html.H2('Distribution of IMDb Ratings Across Genres', style={'text-align': 'center', 'color': 'black'}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='plot-box', figure=fig_box, style={'height': 750}),
                    ],
                    width={'size': 9, 'offset': 0, 'order': 2}
                ),
                dbc.Col(
                    [
                        html.H6('Select genre:', className='text-center'),
                        dcc.Dropdown(
                            id='dropdown',
                            options=[{"label": option, "value": option} for option in data["MAIN_GENRE"].unique()],
                            value="drama"
                        ),
                        dcc.Graph(id="plot-sub-box")
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                html.H2('IMDb Ratings vs Release Year by Genre', style={'text-align': 'center', 'color': 'black'}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6(
                            'Select genre:',
                            className='text-center',
                        ),
                        dcc.Checklist(
                            id='checkbox',
                            options=[
                                {"label": option, "value": option}
                                for option in data["MAIN_GENRE"].unique()
                            ],
                            value=["drama"],
                        ),
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.H6(
                            'Select release year range:',
                            className='text-center'
                        ),
                        dcc.RangeSlider(
                            id='year_slider',
                            min=data['RELEASE_YEAR'].min(),
                            max=data['RELEASE_YEAR'].max(),
                            value=[data['RELEASE_YEAR'].min(), data['RELEASE_YEAR'].max()],
                            step=None,
                            marks={str(year): str(year) for year in data['RELEASE_YEAR'].unique()}
                        ),
                    ],
                    width=6
                )
            ],
            align='center'
        ),
        dbc.Row(
            [
                dcc.Graph(id='plot-scatter', figure=fig_scatter)
            ],
        ),
    ],
    fluid=True
)


# Callback for updating the bar chart based on the slider value
@app.callback(
    Output('plot-bar', 'figure'),
    [Input('slider', 'value')]
)
def update_bar_chart(num_countries):
    # Get the countries with the most TV shows
    top_countries = data['country'].value_counts().nlargest(num_countries)
    top_countries_names = list(top_countries.index)
    # Filter the dataset to only include TV shows from these countries
    filtered_data = data[data['country'].isin(top_countries_names)]
    # Create a new bar chart based on the filtered dataset
    fig = px.histogram(filtered_data, x='country', title='Number of TV Shows in Each Country', color='country', color_discrete_sequence=px.colors.qualitative.Alphabet)
    # Configure the layout of the new bar chart
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Number of TV shows",
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor="white"
    )
    # Return the new bar chart
    return fig


# Callback for updating the sub box chart based on the dropdown value
@app.callback(
    Output('plot-sub-box', 'figure'),
    [Input('dropdown', 'value')]
)
def update_sub_box_chart(genre):
    # Filter the dataset to only include TV shows of the selected genre
    filtered_data = data[data['MAIN_GENRE'] == genre]
    # Create a new box chart based on the filtered dataset
    fig = px.box(filtered_data, x='GENRE', y='IMDB_RATING', title='Distribution of IMDb Ratings Across ' + genre.title() + ' TV Shows')
    # Configure the layout of the new box chart
    fig.update_layout(
        xaxis_title="Sub-Genre",
        yaxis_title="IMDb Rating",
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor="white"
    )
    # Return the new box chart
    return fig


# Callback for updating the scatter plot based on the checkbox and slider values
@app.callback(
    Output('plot-scatter', 'figure'),
    [Input('checkbox', 'value'),
    Input('year_slider', 'value')]
)
def update_scatter_plot(genres, year_range):
    # Filter the dataset to only include TV shows with the selected genres and release year range
    filtered_data = data[(data['MAIN_GENRE'].isin(genres)) & (data['RELEASE_YEAR'] >= year_range[0]) & (data['RELEASE_YEAR'] <= year_range[1])]
    # Create a new scatter plot based on the filtered dataset
    fig = px.scatter(
        filtered_data,
        x='IMDB_RATING',
        y='RELEASE_YEAR',
        color="MAIN_GENRE",
        title='IMDb Ratings vs Release Year by Genre'
    )
    # Configure the layout of the new scatter plot
    fig.update_layout(
        xaxis_title="IMDb Rating",
        yaxis_title="Release Year",
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor="white"
    )
    # Return the new scatter plot
    return fig


if __name__ == '_main_':
    app.run_server(debug=True)
