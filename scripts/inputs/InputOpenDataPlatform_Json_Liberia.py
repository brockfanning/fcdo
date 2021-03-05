from . import InputOpenDataPlatform_Json

class InputOpenDataPlatform_Json_Liberia(InputOpenDataPlatform_Json.InputOpenDataPlatform_Json):

    def get_indicator_id(self, row):
        return row['target']['indicator']

    def get_indicator_name(self, row):
        return row['target']['name']

    def get_dimensions(self, row):
        return {
            'SERIES': row['target']['series-code'],
            'REF_AREA': '430',
        }
