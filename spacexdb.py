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
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 40}),

                                html.Div(

                                dcc.Dropdown(id='site-dropdown',  
                                options=[
                                {'label': 'All Sites', 'value': 'ALL'},  
                                *[{'label': site, 'value': site} for site in launch_sites]  
                                ],
                                value='ALL', 
                                placeholder="Select a Launch Site here", 
                                searchable=True)),

                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                min=0, 
                                max=10000, 
                                step=1000,
                                marks={i:f'{i}' for i in range(0,10001,2500)},
                                value=[min_payload, max_payload]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),

                                ])
                                



@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        grouped_df = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').size().reset_index(name='Success Count')

        fig = px.pie(grouped_df,
                    values='Success Count', 
                    names='Launch Site', 
                    title='Total Launches for All Launch Sites')

        return fig
    
    else:

        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_count = filtered_df[filtered_df['class'] == 1].shape[0]
        failure_count = filtered_df[filtered_df['class'] == 0].shape[0]
        
        fig = px.pie(
            values=[success_count, failure_count],
            names=['Success', 'Failure'],
            title=f'Success vs Failure for {entered_site}'
            )
        return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])

def update_scatter_chart(entered_site, payload_range):

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Launch Sites',
            labels={'class': 'Launch Success'})
        
    else:
      
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',  
            title=f'Correlation between Payload and Success for {entered_site}',
            labels={'class': 'Launch Success'}
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()