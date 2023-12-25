from dataManager import DataManager
import pandas as pd
import numpy as np
import pyproj
from tqdm import tqdm

url = 'https://www.data.gouv.fr/fr/datasets/r/98f3161f-79ff-4f16-8f6a-6d571a80fea2'

# INITIALISATION
dataManager = DataManager(url)
files = dataManager.getPharmacyFile()
df = pd.read_csv('data/pharmacies', sep=';', encoding='latin-1', header=None, skiprows=1, low_memory=False) 
print("COLONNES => ", df.columns, "\n")

# --------  DATAFRAME  ----------#
new_column_names = [str(i) for i in range(32)]

df.columns = new_column_names
dataTypes = [df['0'].unique()[0], df['0'].unique()[1]]  # Replace with your desired values

# --------  SEPARATION  ----------#
separated_dfs = {}
for value in dataTypes:
    mask = df['0'] == value
    separated_dfs[value] = df[mask]
df = separated_dfs['structureet']
dfLoc = separated_dfs['geolocalisation']

# --------  CLEANING  ----------#
dfLoc = dfLoc.drop(columns=[
    '0',
    '4', 
    '5', 
    '6', 
    '7', 
    '8', 
    '9', 
    '10', 
    '11', 
    '12', 
    '13',
    '14',
    '15',
    '16',
    '17',
    '18',
    '19',
    '20',
    '21',
    '22',
    '23',
    '24',
    '25',
    '26',
    '27',
    '28',
    '29',
    '30',
    '31'
])
dfLoc.columns = [
    'id',
    'latitude',
    'longitude'
]
df.drop(columns=['0', '2', '5', '6', '10', '11', '12', '13', '14', '17', '18', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '31'], inplace=True)
df.columns = [
    'id',
    'shortName', 
    'Name',
    'adress1', 
    'adress2',
    'adress3',
    'city',
    'phone',
    'type',
    'date'
]
data_types = {
    "id": str,
    "shortName": str,
    "Name": str,
    "adress1": float,
    "adress2": str,
    "adress3": str,
    "city": str,
    "phone": str,
    "type": str,
    "date": str,
    
}
df = df.astype(data_types)

# --------  MERGE  ----------#
df = df.merge(dfLoc, on='id', how='inner')

# --------  FILTER TYPE  ----------#
specific_values = ["Pharmacie d'Officine", 'Pharmacie Mutualiste']
df = df[df['type'].isin(specific_values)]
df.sort_values(by=['type'], inplace=True)

# --------  FORMAT ADRESS  ----------#
df['adress1'] = df['adress1'].astype(str)
replacements = {
    'R': 'rue',
    'BD': 'boulevard',
    'AV': 'avenue',
    'PL': 'place',
    'CHEM': 'chemin',
    'ALL': 'allée',
    'IMP': 'impasse',
    'LD': 'lieu-dit',
    'RTE': 'route',
    'CRS': 'cours',
    'CCAL': 'centre commercial',
    'CAR': 'carrefour',
    'SQ': 'square',
    'ZI': 'Zone Industrielle',
    'FG': 'faubourg',
    'QU': 'quartier',
    'PR': 'promenade',
    'ZAC': 'Zone Artisanale ou Commerciale',
    'LOT': 'lotissement',
    'CITE': 'cité',
    'PAS': 'passage',
    'CHAUS': 'chaussée',
    'QUAI': 'quai',

}
df['adress2'] = df['adress2'].replace(replacements)

exceptions = {'du', 'de', 'et', 'la', 'le', 'des'}
def format_address(adress):
    adress = str(adress)
    words = adress.lower().split()
    final_words = []
    for word in words:
        final_words.append(word if word in exceptions else word.capitalize())
    return ' '.join(final_words)
df['adress3'] = df['adress3'].apply(format_address)

def join_address(row):
    adress1 = row["adress1"]

    if ((adress1 == 'nan') and (row["adress2"] == 'nan')):
        row["adress"] = ""
        return row
    
    adress1 = str(int(float(adress1))) if not adress1=='nan' else ''
    
    if adress1 == "":
        row["adress"] = f"{adress1} {row['adress2']} {row['adress3']}, {row['city']}"
    else:
        row["adress"] = f"{row['adress2']} {row['adress3']}, {row['city']}"
    
    return row

df = df.apply(lambda row: join_address(row), axis=1)
print(df.head())
specific_values = [
    "Pharmacie d'Officine",
    'Pharmacie Mutualiste',
    'Centre Hospitalier (C.H.)',
    'Centre Hospitalier Régional (C.H.R.)',
    'Centre Hospitalier Universitaire (C.H.U.)',
    'Etablissement de Soins Pluridisciplinaire',
    'Maison de santé (L.6223-3)'
]
df = df[df['type'].isin(specific_values)]
df.sort_values(by=['type'], inplace=True)

# --------  FORMAT ADRESS  ----------#
df['adress1'] = df['adress1'].astype(str)
replacements = {
    'R': 'rue',
    'BD': 'boulevard',
    'AV': 'avenue',
    'PL': 'place',
    'CHEM': 'chemin',
    'ALL': 'allée',
    'IMP': 'impasse',
    'LD': 'lieu-dit',
    'RTE': 'route',
    'CRS': 'cours',
    'CCAL': 'centre commercial',
    'CAR': 'carrefour',
    'SQ': 'square',
    'ZI': 'Zone Industrielle',
    'FG': 'faubourg',
    'QU': 'quartier',
    'PR': 'promenade',
    'ZAC': 'Zone Artisanale ou Commerciale',
    'LOT': 'lotissement',
    'CITE': 'cité',
    'PAS': 'passage',
    'CHAUS': 'chaussée',
    'QUAI': 'quai',

}
df['adress2'] = df['adress2'].replace(replacements)

exceptions = {'du', 'de', 'et', 'la', 'le', 'des'}
def format_address(adress):
    adress = str(adress)
    words = adress.lower().split()
    final_words = []
    for word in words:
        final_words.append(word if word in exceptions else word.capitalize())
    return ' '.join(final_words)
df['adress3'] = df['adress3'].apply(format_address)

def join_address(row):
    adress1 = row["adress1"]

    if ((adress1 == 'nan') and (row["adress2"] == 'nan')):
        row["adress"] = ""
        return row
    
    adress1 = str(int(float(adress1))) if not adress1=='nan' else ''
    
    if adress1 == "":
        row["adress"] = f"{adress1} {row['adress2']} {row['adress3']}, {row['city']}"
    else:
        row["adress"] = f"{row['adress2']} {row['adress3']}, {row['city']}"
    
    return row

df = df.apply(lambda row: join_address(row), axis=1)
print(df.head())

#--------  LAMBERT 93 => WGS 84  ----------#
lambert93 = pyproj.Proj(init='epsg:2154')
wgs84 = pyproj.Proj(init='epsg:4326')
t = tqdm(total=df.shape[0], desc="Conversion LAMBERT 93 => WGS 84")
def convert_coordinates(x, y):
    longitude, latitude = pyproj.transform(lambert93, wgs84, x, y)
    t.update(1)
    return pd.Series({'Latitude': latitude, 'Longitude': longitude})

# --------  FORMAT PHONE  ----------#
def format_with_zeros(value):
    if pd.isnull(value):
        return value
    elif value == 'nan':
        return ""
    value = int(float(value))
    
    # Format the integer value with leading zeros
    return '{:010d}'.format(value)

df['phone'] = df['phone'].apply(format_with_zeros)

# --------  FORMAT GPS  ----------#
df[['latitude', 'longitude']] = df.apply(lambda x: convert_coordinates(x['latitude'], x['longitude']), axis=1)

# --------  EXPORT  ----------#
df.to_json('data/out/pharmacies.json', orient='records')