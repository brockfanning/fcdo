from sdg.open_sdg import open_sdg_build
import os
import shutil
import yaml
from sdg import helpers
import pandas as pd

def is_country_afdb(country):
    return country in [
        'burundi',
        'ethiopia',
        'mozambique',
        'uganda',
        'zambia',
        'zimbabwe',
    ]


def is_country_pxweb(country):
    return country in [
        'palestine',
        'jordan',
    ]


def fix_time_period(x):
    x = str(x)
    years = x.split('-')
    return str(int(years[0]))


def set_time_detail(df):
    if 'TIME_DETAIL' not in df.columns.to_list():
        df = df.copy()
        df['TIME_DETAIL'] = df['Year']
    df['Year'] = df['Year'].apply(fix_time_period)
    return df


def columns_to_drop(country):
    columns = []
    if country == 'jordan':
        columns.extend([
            'Gross Disbursement',
        ])
    if is_country_afdb(country):
        columns.extend([
            'scale',
        ])
    if country == 'mozambique':
        columns.extend([
            'objectivo',
            'meta',
            'indicador'
        ])
    return columns


def common_alterations(df):
    df['REPORTING_TYPE'] = 'N'
    return df


def drop_columns(df, country):
    columns_in_data = df.columns.to_list()
    for column in columns_to_drop(country):
        if column in columns_in_data:
            df = df.drop([column], axis=1)
    return df


def limit_to_national_ref_area(df, ref_area):
    def row_matches_ref_area(row):
        return row['REF_AREA'] == ref_area

    df = df.copy()
    mask = df.apply(row_matches_ref_area, axis=1)
    return df[mask]


def set_series_and_unit(df, context):
    if 'SERIES' not in df.columns.to_list():
        indicator_id = context['indicator_id']
        series = helpers.sdmx.get_series_code_from_indicator_id(indicator_id)
        df['SERIES'] = series
    if 'UNIT_MEASURE' not in df.columns.to_list():
        df['UNIT_MEASURE'] = ''
    for index, row in df.iterrows():
        if row['UNIT_MEASURE'] == '':
            series = row['SERIES']
            unit = helpers.sdmx.get_unit_code_from_series_code(series)
            df.at[index, 'UNIT_MEASURE'] = unit
    return df


def apply_complex_mappings(df, country):
    try:
        filename = 'complex-' + country + '.yml'
        filepath = os.path.join('scripts', 'sdg-build-config', 'sdmx-mappings', filename)
        with open(filepath, 'r') as stream:
            complex_mappings = yaml.load(stream, Loader=yaml.FullLoader)
            columns = df.columns.to_list()
            for mapping in complex_mappings:
                source_column = mapping['source_column']
                source_values = mapping['source_values']
                new_columns = source_values[next(iter(source_values))].keys()

                if source_column in columns:
                    def map_values(row):
                        source_value = row[source_column]
                        if source_value in source_values:
                            mapped_values = source_values[source_value]
                            for key in mapped_values:
                                row[key] = mapped_values[key]
                        return row
                    for column in new_columns:
                        df[column] = ''
                    df = df.apply(map_values, axis='columns')
                    df = df.drop(columns=[source_column])
        return df
    except:
        return df


def alter_data_jordan(df, context):
    column_fixes = {
        'Yeat': 'Year',
        'السنة': 'Year',
    }
    df = df.rename(columns=column_fixes)
    df = apply_complex_mappings(df, 'jordan')
    df = common_alterations(df)
    df = set_time_detail(df)
    df = drop_columns(df, 'jordan')
    df = set_series_and_unit(df, context)
    return df


def alter_data_palestine(df, context):
    column_fixes = {
        'Yeat': 'Year',
        'السنة': 'Year',
    }
    df = df.rename(columns=column_fixes)
    df = common_alterations(df)
    df = set_time_detail(df)
    df = drop_columns(df, 'palestine')
    df = set_series_and_unit(df, context)
    return df


def alter_data_burundi(df, context):
    df = common_alterations(df)
    df = set_series_and_unit(df, context)
    df = set_time_detail(df)
    return drop_columns(df, 'burundi')


def alter_data_ethiopia(df, context):
    df = common_alterations(df)
    df = set_series_and_unit(df, context)
    df = set_time_detail(df)
    return drop_columns(df, 'ethiopia')


def alter_data_mozambique(df, context):
    df = common_alterations(df)
    df = set_series_and_unit(df, context)
    df = set_time_detail(df)
    return drop_columns(df, 'mozambique')


def alter_data_uganda(df, context):
    df = common_alterations(df)
    df = set_series_and_unit(df, context)
    df = set_time_detail(df)
    return drop_columns(df, 'uganda')


def alter_data_zambia(df, context):
    df = common_alterations(df)
    df = set_series_and_unit(df, context)
    df = set_time_detail(df)
    return drop_columns(df, 'zambia')


def alter_data_zimbabwe(df, context):
    df = common_alterations(df)
    df = set_series_and_unit(df, context)
    df = set_time_detail(df)
    return drop_columns(df, 'zimbabwe')


def alter_data_lao(df, context):
    df = common_alterations(df)
    return drop_columns(df, 'lao')


def alter_data_cambodia(df, context):
    df = common_alterations(df)
    return drop_columns(df, 'cambodia')


def alter_data_rwanda(df, context):
    df = common_alterations(df)
    df = limit_to_national_ref_area(df, 'RW')
    return drop_columns(df, 'rwanda')


def alter_data_by_country(country):
    if country == 'jordan':
        return alter_data_jordan
    elif country == 'palestine':
        return alter_data_palestine
    elif country == 'mozambique':
        return alter_data_mozambique
    elif country == 'ethiopia':
        return alter_data_ethiopia
    elif country == 'burundi':
        return alter_data_burundi
    elif country == 'uganda':
        return alter_data_uganda
    elif country == 'zambia':
        return alter_data_zambia
    elif country == 'zimbabwe':
        return alter_data_zimbabwe
    elif country == 'lao':
        return alter_data_lao
    elif country == 'cambodia':
        return alter_data_cambodia
    elif country == 'rwanda':
        return alter_data_rwanda


def alter_indicator_id(indicator_id):
    return indicator_id.replace('.', '-')


def alter_meta(meta):
    for key in meta:
        if meta[key] is not None and isinstance(meta[key], str):
            meta[key] = meta[key].replace("'", "&#39;")
    return meta

countries = [
    'jordan',
    'palestine',
    'burundi',
    'ethiopia',
    'mozambique',
    'uganda',
    'zambia',
    'zimbabwe',
    'cambodia',
    'lao',
    'rwanda',
]
for country in countries:
    config_path = os.path.join('scripts', 'sdg-build-config', country + '.yml')
    alter_data = alter_data_by_country(country)
    print('******* ' + country + ' *******')
    open_sdg_build(config=config_path, alter_data=alter_data, alter_meta=alter_meta, alter_indicator_id=alter_indicator_id)
    source = os.path.join('_build', country)
    destination = os.path.join('web', '_site', country, 'sdg-build')
    shutil.move(source, destination)
