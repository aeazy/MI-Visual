import base64
import io
import os
from datetime import datetime
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd
import plotly_express as px
from dash.exceptions import PreventUpdate


def __init__(self, df) -> None:
    self.df = df
    
def store_uploaded_data(contents, list_of_names, list_of_dates):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    return df.to_json(date_format='iso', orient='split')

def read_file():
    with open('testFiles/2023-02-15_cal018_m_calr.csv') as file:
        df = pd.read_csv(file)
        return df.to_json(date_format='iso', orient='split')

def df_from_stored_data(stored_data):
    df = pd.read_json(stored_data, orient='split')
    # convert to datetime index
    return df.where(df['envirolightlux_1'] >= 0, 1)   # converts envirolight to binary 

def df_index_datetime(df):
    df['Date_Time_1'] = df['Date_Time_1'].str.strip()
    df['Date_Time_1'] = pd.to_datetime(df['Date_Time_1'], format='%m/%d/%Y %H:%M:%S')
    df = df.set_index('Date_Time_1')
    return df

def channels(df):
    columns = df.columns
    headers = [column[:-2].replace('_','') for column in columns]
    headers = np.unique(headers)
    return [header for header in headers if header != 'DateTime']

def find_channels(channel, df):
    if channel == 'kcalhr':
        channel_data = list(filter(lambda x: 'kcal_hr' in x, df.columns))
        return df[channel_data]     # returns df of channels
    else: 
        channel_data = list(filter(lambda x: channel in x, df.columns)) 
        return df[channel_data]     # returns df of channels

def set_x_label(value):
    xLabel_dict = {'vo2':'ΔO2', 'vco2': 'ΔCO2', 'vh2o': 'ΔH2O', 'allmeters':'Total Distance (m)', 'pedmeters':'Pedestrian Locomotion (m)', 'bodymass':'Mass (g)', 'waterina':'Water Consumed (mL)',
                   'foodupa':'Food Consumed (g)', 'envirotemp':'Temperature ('+chr(176)+'C)', 'kcalhr':'Energy Expenditure (kcal/hr)', 'si13c':'ppm'}
    x_label = ""
    try: 
        x_label = xLabel_dict[value]
    finally:
        return x_label
    
def set_title(channel_1, channel_2=None):
    title_dict = {'vo2':'Oxygen Consumption', 'vco2': 'Carbon Dioxide Production', 'vh2o': 'Water Loss', 'allmeters':'Total Distance', 'pedmeters':'Pedestrian Locomotion', 'bodymass':'Body Mass', 'waterina':'Water Consumption',
                   'foodupa':'Food Consumption', 'envirotemp':'Environment Temperature', 'kcalhr':'Energy Expenditure', 'si13c':'ppm', 'rq':'Respiratory Exchange Ratio', 
                   'kcalhr':'Energy Expenditure', 'wheelmeters':'Wheel Meters'
                    }
    title = ""
    
    # base case
    if channel_1 not in title_dict.keys() and channel_2 not in title_dict.keys():
        return title
    
    if channel_1 in title_dict.keys():
        title += title_dict[channel_1]
        
    if channel_2 in title_dict.keys():
        title += " & {0}".format(title_dict[channel_2])
        
    else:
        return title
    
    return title


def group_treatment_df(df, channel, group_dict):
    grouped_treatment = {}      # Empty dict to hold all treatments 
    for i in range(1, len(group_dict) + 1):
        cages = group_dict[f'group_{i}'][1].split(',')
        cages = [cage.strip() for cage in cages]    # strip blanks from cage nums
        cage_channels = []      # Empty list to record channels associated with treatment
        
        # Iterate through cages and add channels to cage_channels list
        for n in cages:
            if channel != 'kcal':
                s = f"{channel}_{n}"
                cage_channels.append(s)
            elif channel == 'kcal':
                s =f"{channel}_hr_{n}"
                cage_channels.append(s)
                
        # Create df for treatment and average all cages into single column
        group_df = df[cage_channels].mean(axis=1, numeric_only=True)
        
        # Add df to grouped_treatment dict
        grouped_treatment.update({f"{group_dict[f'group_{i}'][0]}":group_df})
        
    # Combine each treatment's df into one
    group_df = pd.DataFrame.from_dict(grouped_treatment)
    return group_df

# ----------------------------------------------------------------------
# Debugging
# file = read_file()
# df = df_from_stored_data(file)
# df = df_index_datetime(df)




