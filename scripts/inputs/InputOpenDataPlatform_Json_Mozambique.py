from . import InputOpenDataPlatform_Json

class InputOpenDataPlatform_Json_Mozambique(InputOpenDataPlatform_Json.InputOpenDataPlatform_Json):

    def get_dimension_map(self):
        return {
            'sériedescrição': 'SERIES',
            'província': 'REF_AREA',
            'sexo': 'SEX',
            'idade': 'AGE',
            'área-de-residência': 'URBANISATION',
            'nível-de-educação': 'EDUCATION_LEV',
            'ocupação': 'OCCUPATION',
            'deficiência': 'DISABILITY_STATUS',
            'composição-composta': 'COMPOSITE_BREAKDOWN',
            'quintil': 'INCOME_WEALTH_QUANTILE',
        }

    def get_indicator_id(self, row):
        return row['indicador-disponível']['id']

    def get_indicator_name(self, row):
        return row['indicador-disponível']['name']
