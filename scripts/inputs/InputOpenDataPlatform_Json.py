from urllib.request import urlopen
import json
from sdg.inputs import InputBase

"""
TODO:
1. Filter out national data
2. Resolve any more code mapping issues
"""

class InputOpenDataPlatform_Json(InputBase):


    def __init__(self, source=None, logging=None):
        InputBase.__init__(self, logging=logging)
        self.source = source


    def execute(self, indicator_options):
        payload = self.fetch_file(self.source)
        parsed = json.loads(payload)
        dimension_map = self.get_dimension_map()
        indicators = {}
        names = {}
        for item in parsed['data']:
            indicator_id = self.normalize_indicator_id(self.get_indicator_id(item))
            indicator_name = self.normalize_indicator_name(self.get_indicator_name(item), indicator_id)
            indicator_name = indicator_name.strip(':').strip('.').strip()
            if indicator_id not in indicators:
                indicators[indicator_id] = []
            dimensions = self.get_dimensions(item)

            idx = 0
            for year in self.get_years(item):
                value = item['values'][idx]
                if value is not None:
                    disaggregations = dimensions.copy()
                    disaggregations['UNIT_MEASURE'] = self.get_unit(item)
                    disaggregations['UNIT_MULT'] = self.get_unit_multiplier(item)
                    self.set_required_columns(disaggregations)
                    row = self.get_row(year, value, disaggregations)
                    indicators[indicator_id].append(row)
                idx += 1

        for indicator_id in indicators:
            df = self.create_dataframe(indicators[indicator_id])
            self.add_indicator(indicator_id, name=indicator_name, data=df, options=indicator_options)


    def get_dimensions(self, row):
        dimension_map = self.get_dimension_map()
        dimensions = {}
        for prop in row:
            if prop in dimension_map:
                dimensions[dimension_map[prop]] = self.fix_disaggregation_value(prop, row[prop]['id'])
        return dimensions


    def get_dimension_map(self):
        return {
            'seriesdescription': 'SERIES',
            'area': 'REF_AREA',
            'geoarea': 'REF_AREA',
            'sex': 'SEX',
            'age': 'AGE',
            'urbanisation': 'URBANISATION',
            'urbanization': 'URBANISATION',
            'education-level': 'EDUCATION_LEV',
            'occupation': 'OCCUPATION',
            'disability-status': 'DISABILITY_STATUS',
            'comp-breakdown': 'COMPOSITE_BREAKDOWN',
            'wealth-quintile': 'INCOME_WEALTH_QUANTILE',
        }


    def set_required_columns(self, row):
        if 'OBS_STATUS' not in row:
            row['OBS_STATUS'] = 'A'


    def get_years(self, row):
        start = int(row['startDate'][0:4])
        end = int(row['endDate'][0:4])
        if start == end:
            return [start]
        return list(range(start, end))


    def get_unit(self, row):
        unit = row['unit']
        percentages = ['Percent', 'Percentage', '%']
        if unit in percentages:
            return 'PT'
        numbers = ['Number', 'Number (Units)', 'Number (Thousands)']
        if unit in numbers:
            return 'NUMBER'
        return unit


    def get_unit_multiplier(self, row):
        unit_mult = row['scale']
        return unit_mult


    def get_indicator_id(self, row):
        return row['indicator']['id']


    def get_indicator_name(self, row):
        return row['indicator']['name']


    def fix_disaggregation_value(self, column, value):
        if value == '_T':
            return ''
        return value
