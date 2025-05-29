import json
from jsonschema import validate
from pathlib import Path
import requests
from pprint import pprint

if __name__ == '__main__':
    if False:
        json_schema_f = Path("nvd.schema/cve_history_api_json_2.0.schema.json")
        with open(json_schema_f, 'r') as f:
            json_schema = json.load(f)
        nvd_sample_f = Path("dump.update.history.json")
        with open(nvd_sample_f, 'r') as f:
            nvd_sample = json.load(f)
        validate(instance=nvd_sample, schema=json_schema)
        exit()
    if False:
        # json schema from file
        json_schema_f = Path("nvd.schema/cve_api_json_2.0.schema.json")
        with open(json_schema_f, 'r') as f:
            json_schema = json.load(f)

        # json schema from url
        # json_schema_url = "https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema"
        # response = requests.get(json_schema_url)
        # response.raise_for_status()
        # json_schema = response.json()

        nvd_sample_f = Path("nvd.data/CVE-2018-10902.json")
        with open(nvd_sample_f, 'r') as f:
            nvd_sample = json.load(f)

        validate(instance=nvd_sample, schema=json_schema)
        exit()
