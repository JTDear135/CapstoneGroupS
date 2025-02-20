These scripts generate Python classes from the API responses.

## Steps

1. Collect API responses samples through collect.py
2. Combine API responses using combine.py
3. Generate JSON schema using Quicktype:  

    `quicktype .\scripts\schema-generation\quicktype_input.json -o .\scripts\schema-generation\schema.json --lang schema`

4. Generate Python models using datamodel-codegen:  

    `datamodel-codegen --input .\scripts\schema-generation\schema.json --input-file-type jsonschema --output model_new_generated.py`
5. Manually adjust Python model

[ICAO Reference](https://www.faa.gov/air_traffic/flight_info/aeronav/notams/media/ICAO_NOTAM_Format_Example.pdf)