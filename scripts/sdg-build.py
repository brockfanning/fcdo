from sdg.open_sdg import open_sdg_build
import os
import shutil

def alter_data_jordan(df):
    column_fixes = {
        'Yeat': 'Year',
        'السنة': 'Year',
    }
    df = df.rename(columns=column_fixes)


    return df

def alter_data_by_country(country):
    if country == 'jordan':
        return alter_data_jordan
    if country == 'palestine':
        return alter_data_jordan
    return None


def alter_indicator_id(indicator_id):
    return indicator_id.replace('.', '-')

countries = [
    'jordan',
    'palestine',
    'burundi',
    'ethiopia',
    'mozambique',
    'uganda',
    'zambia',
    'zimbabwe',
]
for country in countries:
    config_path = os.path.join('scripts', 'sdg-build-config', country + '.yml')
    alter_data = alter_data_by_country(country)
    open_sdg_build(config=config_path, alter_data=alter_data, alter_indicator_id=alter_indicator_id)
    source = os.path.join('_build', country)
    destination = os.path.join('web', '_site', country, 'sdg-build')
    shutil.move(source, destination)
