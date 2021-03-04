from urllib.request import urlopen
import json
from sdg.inputs import InputBase

class InputOpenDataPortal_Json(InputBase):


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
            indicator_id = self.normalize_indicator_id(item['indicator']['id'])
            indicator_name = self.normalize_indicator_name(item['indicator']['name-en'], indicator_id)
            indicator_name = indicator_name.strip(':').strip('.').strip()
            if indicator_id not in indicators:
                indicators[indicator_id] = []
            series_identifier = {}
            for prop in item:
                if prop in dimension_map:
                    series_identifier[dimension_map[prop]] = self.fix_disaggregation_value(prop, item[prop]['id'])

            idx = 0
            for year in self.get_years(item):
                value = item['values'][idx]
                if value is not None:
                    disaggregations = series_identifier.copy()
                    disaggregations['UNIT_MEASURE'] = self.get_unit(item)
                    row = self.get_row(year, value, disaggregations)
                    indicators[indicator_id].append(row)
                idx += 1

        for indicator_id in indicators:
            df = self.create_dataframe(indicators[indicator_id])
            self.add_indicator(indicator_id, name=indicator_name, data=df, options=indicator_options)


    def get_dimension_map(self):
        return {
            'seriesdescription': 'SERIES',
            'area': 'REF_AREA',
            'sex': 'SEX',
            'age': 'AGE',
            'urbanisation': 'URBANISATION',
            'education-level': 'EDUCATION_LEV',
        }


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
        return unit


    def get_indicator_name(self, row):
        return row['indicator']['name-en']


    def fix_disaggregation_value(self, column, value):
        if value == '_T':
            return ''
        return value
