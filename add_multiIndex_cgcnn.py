import pandas as pd
import numpy as np

# Read in the data
df = pd.read_json('./id_prop_46740.json.gz')

idx1 = pd.read_csv('../refRepos/cgcnn/data/material-data/mp-ids-3402.csv', header=None)
idx2 = pd.read_csv('../refRepos/cgcnn/data/material-data/mp-ids-27430.csv', header=None)
idx3 = pd.read_csv('../refRepos/cgcnn/data/material-data/mp-ids-46744.csv', header=None)

idx1 = df['uniIdx'].isin(idx1[0])
idx2 = df['uniIdx'].isin(idx2[0])
idx3 = df['uniIdx'].isin(idx3[0])

df['isin_3402'] = idx1
df['isin_27430'] = idx2
df['isin_46744'] = idx3

cols = pd.MultiIndex.from_tuples([
    ('uniIdx', 'uniIdx'),
    ('composition', 'composition'),
    ('structure', 'structure'),
    ('properties', 'band_gap'),
    ('properties', 'energy'),
    ('properties', 'energy_per_atom'),
    ('properties', 'formation_energy_per_atom'),
    ('scheme', 'isin_3402'),
    ('scheme', 'isin_27430'),
    ('scheme', 'isin_46744')
])

df.columns = cols
selected = df[df['scheme']['isin_3402'] == True]['properties']