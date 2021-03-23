import os
import yaml
from shutil import copyfile
from inputs.InputOpenDataPlatform_Json import InputOpenDataPlatform_Json
from inputs.InputOpenDataPlatform_Json_Mozambique import InputOpenDataPlatform_Json_Mozambique
from inputs.InputOpenDataPlatform_Json_Liberia import InputOpenDataPlatform_Json_Liberia
from sdg.inputs.InputJsonStat import InputJsonStat
from sdg.outputs import OutputSdmxMl
from sdg.schemas import SchemaInputSdmxMsd
from sdg.translations import TranslationInputSdmx
from sdg.translations import TranslationInputSdmxMsd
import requests
import re
from bs4 import BeautifulSoup

msd_path = os.path.join('scripts', 'SDG_MSD.xml')
dsd_path = os.path.join('scripts', 'SDG_DSD.xml')
schema_input = SchemaInputSdmxMsd(schema_path=msd_path)
translations = [
    TranslationInputSdmx(source=dsd_path),
    TranslationInputSdmxMsd(source=msd_path)
]

def convert_jordan_link_to_endpoint(link):
    href = link.get('href')
    href = href.replace('/pxweb/', '/api/v1/')
    href = href.replace('SDG__', '')
    href = href.replace('__', '/')
    href = 'http://jorinfo.dos.gov.jo' + href
    return href

def get_jordan_endpoints():
    with open(os.path.join('web', '_data', 'countries', 'jordan', 'index.html'), 'r') as f:
        soup = BeautifulSoup(f.read(), 'html5lib')
    link_prefix = '/Databank/pxweb/en/SDG/'
    endpoints = []
    for link in soup.findAll('a', attrs={'href': re.compile('^' + link_prefix)}):
        endpoint = convert_jordan_link_to_endpoint(link)
        endpoints.append(endpoint)
    return endpoints

def convert_palestine_link_to_endpoint(link):
    href = link.get('href')
    href = href.replace('/pxweb/', '/api/v1/')
    href = href.replace('__', '/')
    return href

def get_palestine_endpoints():
    r = requests.get('http://pcbs.gov.ps/SDGs.aspx?pageId=0')
    soup = BeautifulSoup(r.content, 'html5lib')
    link_prefix = 'http://pcbs.gov.ps/SDGsIndicators/pxweb/en/myDb/'
    endpoints = []
    for link in soup.findAll('a', attrs={'href': re.compile('^' + link_prefix)}):
        endpoint = convert_palestine_link_to_endpoint(link)
        endpoints.append(endpoint)
    return endpoints

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
                output_folder=temp_output_folder,
                structure_specific=True,
            )
            odp_output.execute()
            path_from = os.path.join(temp_output_folder, 'sdmx', 'all.xml')
            path_to = os.path.join(destination_output_folder, item + '.xml')
            copyfile(path_from, path_to)
        elif info['platform']['system'] == 'PX Web':
            continue
            post_data = {
                "query": [],
                "response": {
                    "format": "json-stat"
                }
            }
            endpoints = get_jordan_endpoints() if item == 'jordan' else get_palestine_endpoints()
            year_column = 'Time' if item == 'jordan' else 'TIME PERIOD'
            pxweb_input = InputJsonStat('', endpoints, None, post_data=post_data,
                year_column=year_column, value_column='value', sleep=5)
            pxweb_output = OutputSdmxMl(
                [pxweb_input],
                schema_input,
                translations=translations,
                dsd=dsd_path,
                output_folder=temp_output_folder
            )
            pxweb_output.execute()
            path_from = os.path.join(temp_output_folder, 'sdmx', 'all.xml')
            path_to = os.path.join(destination_output_folder, item + '.xml')
            copyfile(path_from, path_to)
