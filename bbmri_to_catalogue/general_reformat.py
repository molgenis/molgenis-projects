import pandas as pd


def reformat_countries(country):
    if country == 'United Kingdom':
        country = 'United Kingdom of Great Britain and Northern Ireland (the)'
    elif country == 'Czech Republic':
        country = 'Czechia'
    elif country == 'Europe':
        country = ''
    elif country == 'Netherlands':
        country = 'Netherlands (the)'
    elif country == 'Russia':
        country = 'Russian Federation (the)'
    elif country == 'United States of America':
        country = 'United States of America (the)'
    elif country == 'Vietnam':
        country = 'Viet Nam'

    return country


def get_diagnoses(list_of_dict):
    data = ''
    for d in list_of_dict:
        diagnosis_id = d.get('id')[15:]
        diagnosis_label = d.get('label')
        diagnosis = diagnosis_id + ' ' + diagnosis_label
        data += ',' + '"' + diagnosis + '"'

    if not data == '':
        return data[1:]

    return data


def reformat_diseases(diseases):
    diseases = diseases.replace('U07.1 Emergency use of U07 - COVID-19, virus identified',
                                'U07.1 Laboratory-confirmed COVID-19 diagnosis')
    diseases = diseases.replace('U07.2 Emergency use of U07 - COVID-19, virus not identified',
                                'U07.2 suspect or probable COVID-19 diagnosis')
    diseases = diseases.replace('Malignant neoplasm: ', '')
    diseases = diseases.replace('Secondary and unspecified malignant neoplasm: ', '')
    diseases = diseases.replace('Other malignant neoplasms of skin - ', '')
    diseases = diseases.replace('Malignant neoplasm of other and ill-defined sites: ', '')
    diseases = diseases.replace('- Type 2 diabetes mellitus: With', 'with')
    diseases = diseases.replace('- Unspecified diabetes mellitus: With', 'with')
    diseases = diseases.replace('- Type 1 diabetes mellitus: With', 'with')
    diseases = diseases.replace("Neoplasm of uncertain or unknown behaviour: ", '')
    diseases = diseases.replace('Carcinoma in situ of middle ear and respiratory system - Carcinoma in situ: Bronchus and lung',
                                'Bronchus and lung')
    diseases = diseases.replace('Carcinoma in situ of cervix uteri - Carcinoma in situ: ', '')

    return diseases


def get_hyperlink(x):
    """
    Return hyperlink for websites if not filled out correctly.
    """
    if not pd.isna(x):
        if not x.startswith('http'):
            x = 'https://' + x

    return x


def get_from_dict(d, key):
    if not pd.isna(d):
        data = d.get(key)
        return data

    return ''


def get_from_list_of_dict(list_of_dict, key):
    data = ''

    for d in list_of_dict:
        data += ',' + d.get(key)

    return data[1:]


def float_to_int(df):
    """
    Cast float64 Series to Int64.
    """
    for column in df.columns:
        if df[column].dtype == 'float64':
            df.loc[:, column] = df[column].astype('Int64')

    return df
