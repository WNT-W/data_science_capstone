# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
            ],
            placeholder='Select a launch site here',
            searchable=True
        ),
        html.Br(),

        # Pie chart showing the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
            marks={
                0: '0 Kg',
                2000: '2000 Kg',
                4000: '4000 Kg',
                6000: '6000 Kg',
                8000: '8000 Kg',
                10000: '10000 Kg'
            }
        ),

        # Scatter chart showing the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie(launch_site):
    if launch_site == 'ALL':
        df = spacex_df[spacex_df['class'] == 1]
        pie_fig = px.pie(
            df,
            values='class',
            names='Launch Site',
            title='Pie Chart: Total Success Launches by Launch Site'
        )
    else:
        df = spacex_df[spacex_df['Launch Site'] == launch_site]
        value_counts = df['class'].value_counts()
        pie_fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title=f'Pie Chart: Success vs Failed Launches at {launch_site}'
        )
    return pie_fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs,
# `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def get_scatter(launch_site, payload):
    if launch_site == 'ALL':
        df = spacex_df[
            (payload[0] <= spacex_df['Payload Mass (kg)']) &
            (spacex_df['Payload Mass (kg)'] <= payload[1])
        ]
        scatter_fig = px.scatter(
            df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
        )
        scatter_fig.update_layout(
            title=f'Scatter Plot: {launch_site} for Payload Range {payload}',
            xaxis_title='Payload Mass in Kg',
            yaxis_title='Class'
        )
    else:
        df = spacex_df[
            (spacex_df['Launch Site'] == launch_site) &
            (payload[0] <= spacex_df['Payload Mass (kg)']) &
            (spacex_df['Payload Mass (kg)'] <= payload[1])
        ]
        scatter_fig = px.scatter(
            df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
        )
        scatter_fig.update_layout(
            title=f'Scatter Plot: {launch_site} for Payload Range {payload}',
            xaxis_title='Payload Mass in Kg',
            yaxis_title='Class'
        )
    return scatter_fig


# Run the app
if __name__ == '__main__':
    app.run_server()
