import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, dash_table, dcc, html
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import (DashProxy, Input, MultiplexerTransform,
                                    Output)

import assets.functions as fn

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

app = DashProxy(__name__, assets_folder='assets')

app.title = 'MI-Visual'

app.layout = html.Div(className='page-container', children=[
    html.Div(className='sidebar', children=[
        html.H1("MI-Visual", id="sidebarHeader"),

        html.P(id='sidebarInstructions', children="Upload your csv file to begin"),
        
        dcc.Upload(
            id='upload-data', 
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'height': '3%',
                'width': '90%',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin-right': 'auto',
                'margin-left': 'auto',
            },
        ),
        
        dcc.Store(id='stored-data'),
                    
        html.Div(className='sidebar', children=[
            html.H1(className='section-header', children='Assign Groups'),

            html.Hr(),  # horizontal line
                
            html.Div(className='experiment-details', children=[
            html.P('Enter cage numbers as comma-separated list'),
            
            html.Table([
                html.Tr([
                    html.Th(['Group name']),
                    html.Th(['Cages'])
                ]),
                
                html.Tr([
                    html.Td(dcc.Input(id='group-1-name', type='text')),
                    html.Td(dcc.Input(id='group-1-cages', type='text')),
                ]),
                
                html.Tr([
                    html.Td(dcc.Input(id='group-2-name')),
                    html.Td(dcc.Input(id='group-2-cages')),
                ]),
                
                html.Tr([
                    html.Td(dcc.Input(id='group-3-name')),
                    html.Td(dcc.Input(id='group-3-cages')),
                ]),
                
                html.Tr([
                    html.Td(dcc.Input(id='group-4-name')),
                    html.Td(dcc.Input(id='group-4-cages')),
                ]),
            ]),
            
            html.Button('Generate Group Plots', className='sidebar-button', id='generateGroupPlots-button', n_clicks=0),
            
            dcc.Store(id='assign-group-stored-data'),
                                        
        ]),
    ]),
    
    html.Div(id='output-main-content'),

    dcc.Download(id='downloaded-individual-plots'),
    
    dcc.Download(id='downloaded-group-plots'),

    ])
])
# handle file upload
@app.callback(Output('stored-data', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(contents, list_of_names, list_of_dates):
    return fn.store_uploaded_data(contents, list_of_names, list_of_dates)
# -----------------------------------------------------------------------------------

# handle group detail assignment
@app.callback(
    Output('assign-group-stored-data', 'data'),
    [Input('group-1-name','value'), Input('group-1-cages', 'value'),
    Input('group-2-name','value'), Input('group-2-cages', 'value'),
    Input('group-3-name','value'), Input('group-3-cages', 'value'),   
    Input('group-4-name','value'), Input('group-4-cages', 'value')]
)
def store_group_details(x1, y1, x2, y2, x3, y3, x4, y4):
    # x1 = group name , y1 = group cage list
    group_dict = {}
    # prevent null values being saved
    if y1 is not None: 
        if x1 is None:
            x1 = 'Group 1'
            group_dict.update({'group_1':[x1,y1]})
        else:
            group_dict.update({'group_1':[x1,y1]})   
    if y2 is not None:     
        if x2 is None:
            x2 = 'Group 2'
            group_dict.update({'group_2':[x2,y2]})
        else:
            group_dict.update({'group_2':[x2,y2]})   
    if y3 is not None:  
        if x3 is None:
            x3 = 'Group 3'
            group_dict.update({'group_3':[x3,y3]})
        else:
            group_dict.update({'group_3':[x3,y3]})   
    if y4 is not None:             
        if x4 is None:
            x4 = 'Group 4'
            group_dict.update({'group_4':[x4,y4]})
        else:
            group_dict.update({'group_4':[x4,y4]})   
    
    return group_dict

# main-content
@app.callback(
    Output('output-main-content', 'children'),
    Input('stored-data', 'data')
)
def output_main_content(stored_data):
    if stored_data is None:
        raise PreventUpdate
    
    df = fn.df_from_stored_data(stored_data)
    channels = fn.channels(df)

    return html.Div(className='main-content', children=[
        html.Div(className='card', children=[
            dcc.Tabs(id='tabs', className='tab-bar', value='individual-plots', children=[
                dcc.Tab(label='Individual Plots', value='individual-plots', className='tab', children=[
                    
                    html.Div(className='plot-dropdowns', children=[
                        dcc.Dropdown(channels, id='dropdown-individualFig', clearable=False, value=channels[0]),                  
                    ]),
                                       
                    dcc.Graph(id='individualPlot'),
                    
                    html.Hr(),  # horizontal line

                    html.H1(className='page-header', children=['Channel Averages']),
                    
                    html.Div(id='individualPlot-datatable'),
                                        
                    # html.Div(className='checklist', children=[
                    #     dcc.Checklist(channels, id='checklist-individualPlots'),                        
                    # ]),                                                 
                ]),
                
                dcc.Tab(label='Multi-channel', className='tab', value='multiChannel', children=[
                    
                    html.Div(className='plot-dropdowns', children=[
                        dcc.Dropdown(channels, id='channel-1', className='fig-dropdown'),
                        
                        dcc.Dropdown(channels, id='channel-2', className='fig-dropdown'),
                    ]),
                    
                    dcc.Graph(id='multiPlot'),
                    
                    html.Hr(),  # horizontal line
                ]),
                
                dcc.Tab(label='Group Plots', className='tab', value='group-plots', children=[
                    
                    html.Div(className='plot-dropdowns', children=[
                        dcc.Dropdown(channels, id='dropdown-groupFig', className='fig-dropdown', clearable=False, value=channels[0]),
                    ]),

                    dcc.Graph(id='groupPlot'),
                    
                    html.Hr(),  # horizontal line
                    
                    html.H1(className='page-header', children=['Channel Averages']),
                    
                    html.Div(id='groupPlot-datatable'),
                    
                ]),  
                      
            ]),
        ]),
    ])
# -----------------------------------------------------------------------------------

# individual plot
@app.callback(
    Output('individualPlot', 'figure'),
    Input('dropdown-individualFig', 'value'),
    Input('stored-data','data')
)
def output_individual_plot(channel, stored_data):
    stored_df = fn.df_from_stored_data(stored_data)
    df = fn.df_index_datetime(stored_df)
    dff = fn.find_channels(channel, df)
    fig = px.line(dff, x=dff.index, y=dff.columns, 
                  labels={
                      "Date_Time_1": "Date",
                      "variable": "Channel",
                      "value": fn.set_x_label(channel)
                    },
                  title=fn.set_title(channel))
    fig.update_layout(title_x = 0.5)
    return fig

@app.callback(
    Output('individualPlot-datatable', 'children'),
    Input('dropdown-individualFig', 'value'),
    Input('stored-data', 'data')
)  
def output_individual_averages(value, stored_data):
    stored_df = fn.df_from_stored_data(stored_data)
    df = fn.df_index_datetime(stored_df)
    dff = fn.find_channels(value, df).mean().round(3)
    dff = pd.DataFrame.from_records([dff])
    dff.columns = [i for i in range(1, len(dff.columns) + 1)]       # change headers to cage num
    return dash_table.DataTable(dff.to_dict('records'))
# -----------------------------------------------------------------------------------

# multi-channel plot
@app.callback(
    Output('multiPlot', 'figure'),
    Input('stored-data', 'data'),
    Input('channel-1', 'value'),
    Input('channel-2', 'value')
)
def output_multi_plot(stored_data, channel_1, channel_2):
    stored_df = fn.df_from_stored_data(stored_data)     # get stored data
    df = fn.df_index_datetime(stored_df)        # set index to datetime
    dff = fn.find_channels(channel_1, df).join(fn.find_channels(channel_2, df))     # join df from both inputs
    fig = px.line(dff, x=dff.index, y=dff.columns, 
                labels={
                    "Date_Time_1": "Date",
                    "variable": "Channel",
                    "value": fn.set_x_label(channel_1)
                },
                title=fn.set_title(channel_1, channel_2))
    fig.update_layout(title_x = 0.5)
    return fig

# group plot
@app.callback(
    Output('groupPlot', 'figure'),
    Input('generateGroupPlots-button', 'n_clicks'),
    Input('stored-data', 'data'),
    Input('dropdown-groupFig', 'value'),
    Input('assign-group-stored-data', 'data')
)
def output_group_plot(n_clicks, stored_data, channel, group_details):
    if n_clicks == 0:
        raise PreventUpdate
    
    if n_clicks > 0:
        stored_df = fn.df_from_stored_data(stored_data)
        df = fn.df_index_datetime(stored_df)
        dff = fn.group_treatment_df(df, channel, group_details)
    
        fig = px.line(dff, x=dff.index, y=dff.columns, 
                    labels={
                        "Date_Time_1": "Date",
                        "variable": "Group",
                        "value": fn.set_x_label(channel)
                    },
                    title=fn.set_title(channel))
        fig.update_layout(title_x = 0.5)
        return fig
    
@app.callback(
    Output('groupPlot-datatable', 'children'),
    Input('stored-data', 'data'),
    Input('dropdown-groupFig', 'value'),
    Input('assign-group-stored-data', 'data')
)  
def output_group_averages(stored_data, channel, group_details):
    stored_df = fn.df_from_stored_data(stored_data)
    df = fn.df_index_datetime(stored_df)
    dff = fn.group_treatment_df(df, channel, group_details).mean().round(3)
    dff = pd.DataFrame.from_records([dff])
    
    return dash_table.DataTable(dff.to_dict('records'))

# -----------------------------------------------------------------------------------

# download individual plots
# @app.callback(
#     Output('downloaded-individual-plots', 'data'),
#     Input('stored-data', 'data'),
#     Input('checklist-individualPlots', 'value'),
# )
# def download_individualFigures(stored_data, value):
#     if stored_data == {}:
#         raise PreventUpdate
    
#     else:
#         df = fn.df_from_stored_data(stored_data)
#         df = fn.df_index_datetime(df)

#         # format for saving html file
#         downloads_path = str(Path.home() / "Downloads")     # find PC downloads folder
#         current_datetime = datetime.today().strftime('%Y-%m-%d_')  # system datetime
#         filename = f"\{current_datetime}individualPlots.html"
#         new_filename = os.path.join(downloads_path + filename)

#         # create fig for each and write to html file
#         with Path(new_filename).open('w') as f:
#             for val in value:
#                 dff = fn.find_channels(val, df)
#                 fig = px.line(dff, x=dff.index, y=dff.columns, 
#                             labels={
#                                 "Date_Time_1": "Date",
#                                 "variable": "Channel",
#                                 "value": fn.set_x_label(val)
#                                 })
#                 f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
# -----------------------------------------------------------------------------------

# # download group plots
# @app.callback(
#     Output('downloaded-group-plots', 'data'),
#     Input('stored-data', 'data'),
#     Input('checklist-groupPlots', 'value'),
#     Input('assign-group-stored-data', 'data')
    
# )
# def download_groupFigures(stored_data, value, group_details):
#     if stored_data == {}:
#         raise PreventUpdate
    
#     else:
#         df = fn.df_from_stored_data(stored_data)
#         df = fn.df_index_datetime(df)

#         # format for saving html file
#         downloads_path = str(Path.home() / "Downloads")     # find PC downloads folder
#         current_datetime = datetime.today().strftime('%Y-%m-%d_')  # system datetime
#         filename = f"\{current_datetime}groupPlots.html"
#         new_filename = os.path.join(downloads_path + filename)

#         # create fig for each and write to html file
#         with Path(new_filename).open('w') as f:
#             for val in value:
#                 dff = fn.group_treatment_df(df, value, group_details)
#                 fig = px.line(dff, x=dff.index, y=dff.columns, 
#                             labels={
#                                 "Date_Time_1": "Date",
#                                 "variable": "Group",
#                                 "value": fn.set_x_label(val)
#                                 })
#                 f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
# -----------------------------------------------------------------------------------


#
if __name__ == '__main__':
    try:
        app.run_server(debug=False, dev_tools_ui=False)
    except ModuleNotFoundError:
        print("There was an error")
        # subprocess.check_call([sys.executable, -m])
 
