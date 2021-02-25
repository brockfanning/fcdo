from sdg.inputs import InputSdmxMl_UnitedNationsApi
import os
import yaml

root = os.path.join('web', '_data', 'countries')
for item in os.listdir(root):
    if os.path.isdir(os.path.join(root, item)):
        info_file = os.path.join(root, item, 'info.yml')
        with open(info_file, 'r') as stream:
            info = yaml.load(stream, Loader=yaml.FullLoader)
        ref_area = info['ref_area']
        sdmx = InputSdmxMl_UnitedNationsApi(dimension_query={
            'REF_AREA': '116',
            #'REPORTING_TYPE': 'N',
        })
        sdmx.execute(None)
        for indicator_id in sdmx.indicators:
            indicator = sdmx.indicators[indicator_id]
            if indicator.has_data():
                #print(indicator.data)
                pass
            else:
                print('nope')

        break
