import pandas as pd
import json
import os

from dotenv import load_dotenv

load_dotenv()

os.environ

with open('src_de_sample_data/10000_metadata.json') as file:
    json_data = json.load(file)

json_data[]

df = pd.json_normalize(json_data)

df = pd.read_json('src_de_sample_data/10000_tracking.txt', lines=True)
