import os
import yaml
from shutil import copyfile
from inputs.InputOpenDataPlatform_Json import InputOpenDataPlatform_Json
from inputs.InputOpenDataPlatform_Json_Mozambique import InputOpenDataPlatform_Json_Mozambique
from inputs.InputOpenDataPlatform_Json_Liberia import InputOpenDataPlatform_Json_Liberia
from sdg.outputs import OutputSdmxMl
from sdg.schemas import SchemaInputSdmxMsd
from sdg.translations import TranslationInputSdmx
from sdg.translations import TranslationInputSdmxMsd

msd_path = os.path.join('scripts', 'SDG_MSD.xml')
dsd_path = os.path.join('scripts', 'SDG_DSD.xml')
schema_input = SchemaInputSdmxMsd(schema_path=msd_path)
translations = [
    TranslationInputSdmx(source=dsd_path),
    TranslationInputSdmxMsd(source=msd_path)
]

root = os.path.join('web', '_data', 'countries')
temp_output_folder = '_site'
destination_output_folder = os.path.join('web', 'data')
for item in os.listdir(root):
    if os.path.isdir(os.path.join(root, item)):
        info_file = os.path.join(root, item, 'info.yml')
        with open(info_file, 'r') as stream:
            info = yaml.load(stream, Loader=yaml.FullLoader)
        if info['platform']['system'] == 'Open Data Platform':
            data_file = os.path.join(root, item, 'data.json')
            if item == 'mozambique':
                odp_input = InputOpenDataPlatform_Json_Mozambique(source=data_file)
            elif item == 'liberia':
                odp_input = InputOpenDataPlatform_Json_Liberia(source=data_file)
            else:
                odp_input = InputOpenDataPlatform_Json(source=data_file)
            odp_output = OutputSdmxMl(
                [odp_input],
                schema_input,
                translations=translations,
                dsd=dsd_path,
                output_folder=temp_output_folder
            )
            odp_output.execute()
            path_from = os.path.join(temp_output_folder, 'sdmx', 'all.xml')
            path_to = os.path.join(destination_output_folder, item + '.xml')
            copyfile(path_from, path_to)
