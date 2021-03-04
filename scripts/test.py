from inputs.InputOpenDataPortal_Json import InputOpenDataPortal_Json

url = 'https://burundi.opendataforafrica.org/api/2.0/data?datasetId=trppeeg'
odp_input = InputOpenDataPortal_Json(source='web/_data/countries/burundi/data.json')
odp_input.execute(None)
