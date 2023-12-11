import pandas as pd
from scipy.spatial.distance import pdist, squareform,euclidean

import math
from app.src.services import gcp
# Assuming you have a DataFrame c
# alled df with columns: timestamp, player, x, y

# Sample DataFrame creation
data = gcp.job_to_bq('select * from src_ftbl.game_tracking')
df = pd.DataFrame(data)

# Function to calculate distance between players
def calculate_distance(df):
    # Pivot the DataFrame to have players as columns
    pivot_df = df.pivot(index=['timestamp', 'trackable_object','frame'], columns='track_id', values=['x', 'y']).fillna(0)

    # Extract x, y coordinates for each player
    player_x = pivot_df['x'].values
    player_y = pivot_df['y'].values

    # Combine x, y coordinates into a flat array
    player_coordinates = list(zip(player_x, player_y))

    # Calculate pairwise Euclidean distances
    distances = pdist(player_coordinates[0], metric='euclidean')
    distances = math.dist(player_coordinates,)
    # Convert distances to a square matrix
    distance_matrix = squareform(distances)

    # Create a DataFrame from the distance matrix
    distance_df = pd.DataFrame(distance_matrix, columns=pivot_df.index)

    return distance_df

# Call the function and display the result
distance_df = calculate_distance(df)
print(distance_df)

group = df[df.trackable_object!=55].groupby(["trackable_object", 'timestamp'])[["x", "y"]]

def player_dist(player_a, player_b):
    return [euclidean(player_a.iloc[i], player_b.iloc[i])
            for i in range(len(player_a))]

ball = df[df.trackable_object==55][["x", "y"]]

harden_dist = group.apply(player_dist, player_b=(ball))