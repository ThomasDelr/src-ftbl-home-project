import pandas as pd
import json
from dotenv import load_dotenv

load_dotenv()

def loading_file(filepath):
    with open(filepath) as file:
        json_data = json.load(file)
    return json_data

filepath = 'src_de_sample_data/10000_metadata.json'

metadata= loading_file(filepath=filepath)

## transform metadata dict to pd df

df = pd.json_normalize(metadata, meta=['id', 'home_team_score_','away_team_score', ['stadium', 'id','name','city', 'capacity']])
df2 = pd.json_normalize(metadata)

for elmt in metadata:
    print(elmt)