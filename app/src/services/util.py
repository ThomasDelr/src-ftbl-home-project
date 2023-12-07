import os
import pandas as pd
import numpy as np

def get_file_path(relative_path):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the desired file
    file_path = os.path.join(script_dir, relative_path)
    return file_path

### calculate distance
def calculate_distance(df,game_id,team_col, player_col, timestamp_col='timestamp', x_col='x', y_col='y'):
    df = pd.DataFrame(df)
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], format='mixed')
    # Sort the DataFrame by player_id and timestamp
    df = df.sort_values(by=[game_id,team_col,player_col, timestamp_col])
    # Calculate the change in x and y
    df['dx'] = df.groupby([game_id, team_col, player_col])[x_col].diff().fillna(0)
    df['dy'] = df.groupby([game_id, team_col, player_col])[y_col].diff().fillna(0)

    df['distance'] = np.sqrt((df.groupby([game_id,team_col, player_col])[x_col].diff() ** 2 + df.groupby([game_id,team_col, player_col])[y_col].diff() ** 2).fillna(0))
    # Calculate time difference in seconds with microseconds
    df['time_diff'] = df.groupby([game_id, team_col, player_col])[timestamp_col].diff().dt.total_seconds().fillna(0)
    # Calculate speed (sqrt(dx^2 + dy^2) / time_diff) and convert to m/s
    df['speed'] = np.sqrt(df['dx']**2 + df['dy']**2) / df['time_diff']
    # Convert speed to km/h
    df['speed'] *= 3.6
    # Calculate acceleration (change in speed / change in time)
    df['acceleration'] = df.groupby([game_id, team_col, player_col])['speed'].diff() / df['time_diff']


    return df.drop(columns=['time_diff'])


