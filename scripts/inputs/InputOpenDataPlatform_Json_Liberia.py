from .InputOpenDataPlatform_Json import InputOpenDataPlatform_Json

class InputOpenDataPlatform_Json_Liberia(InputOpenDataPlatform_Json):

    def get_indicator_id(self, row):
        return row['target']['indicator']

    def get_indicator_name(self, row):
        return row['target']['name']

    def get_dimensions(self, row):
        dimensions = {
            'SERIES': row['target']['series-code'],
            'REF_AREA': '430',
        }
        if row['target']['id'] == 'LR.2':
            dimensions['SEX'] = 'F'
            dimensions['AGE'] = 'Y15T24'
        if row['target']['id'] == 'LR.3':
            dimensions['SEX'] = 'M'
            dimensions['AGE'] = 'Y15T24'
        if row['target']['id'] == 'LR.4':
            dimensions['SEX'] = '_T'
            dimensions['AGE'] = 'Y15T24'
        if row['target']['id'] == 'LR.5':
            dimensions['SEX'] = 'F'
            dimensions['AGE'] = 'Y_GE15'
        if row['target']['id'] == 'LR.6':
            dimensions['SEX'] = 'M'
            dimensions['AGE'] = 'Y_GE15'
        if row['target']['id'] == 'LR.7':
            dimensions['SEX'] = '_T'
            dimensions['AGE'] = 'Y_GE15'
        if row['target']['id'] == 'LR.8':
            dimensions['SEX'] = 'F'
            dimensions['AGE'] = 'Y_GE25'
        if row['target']['id'] == 'LR.9':
            dimensions['SEX'] = 'M'
            dimensions['AGE'] = 'Y_GE25'
        if row['target']['id'] == 'LR.10':
            dimensions['SEX'] = '_T'
            dimensions['AGE'] = 'Y_GE25'

        return dimensions
