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
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(id='dropd',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC', 'value': 'KSC LC-39A'},
                                                ],
                                                value='ALL',
                                                placeholder="Select Launch Site",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    1000: '1000',
                                                    2000: '2000',
                                                    3000: '3000',
                                                    4000: '4000',
                                                    5000: '5000',
                                                    6000: '6000',
                                                    7000: '7000',
                                                    8000: '8000',
                                                    9000: '9000',
                                                    10000: '10000',},
                                                value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                 ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='dropd', component_property='value'))

def get_pie_chart(dropd):
    filtered_df = spacex_df
    if dropd == 'ALL':
        data=filtered_df[filtered_df['class']==1]
        fig = px.pie(
        data, 
        names='Launch Site', 
        title='Successful Launches')
        
    else:
        data=filtered_df[filtered_df['Launch Site']==dropd]
        fig = px.pie(
        data, 
        names='class', 
        title='Successful Launches at site')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='payload_slider', component_property='value'),
              Input(component_id='dropd', component_property='value'))

def get_scatter(payload_slider,dropd):
    filtered_df = spacex_df
    if dropd == 'ALL':
        data=filtered_df      
        fig = px.scatter(
        data, 
        x="Payload Mass (kg)", 
        y="class",
        color="Booster Version Category",
        title='Successful Launches')
        
    else:
        data=filtered_df[filtered_df["Payload Mass (kg)"].between(payload_slider[0] ,payload_slider[1])]
        data=data[data["Launch Site"]==dropd]
        fig = px.scatter(
        data, 
        x="Payload Mass (kg)", 
        y="class",
        color="Booster Version Category",
        title='Successful Launches at site')
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
