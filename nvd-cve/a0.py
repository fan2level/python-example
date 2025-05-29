# -*-coding:utf-8-*-

import requests
import json
import jsonschema
import csv
from pathlib import Path
import time
import datetime
import logging
import argparse
from pprint import pprint

class NVDCVE(object):
    def __init__(self, nvd_cve=None):
        self.reset()
        if nvd_cve is not None:
            self.__load_nvd_buffer(nvd_cve)

    def reset(self):
        self.__is_valid = False
        self.__id = None
        self.__cvssMetric_version = None
        self.__cvssMetric_score = None
        self.__descriptions = None
        
    def load(self, cvefile):
        self.reset()
        if cvefile.exists() == False:
            return
        with open(cvefile, 'r', encoding='utf-8') as f:
            nvd_cve = json.load(f)
            self.__load_nvd_buffer(nvd_cve)

    def __load_nvd_buffer(self, nvd_cve):
        self.__is_valid = False
        if nvd_cve is None:
            return

        self.__nvd_cve = nvd_cve
        if 'vulnerabilities' in nvd_cve:
            self.__is_valid = False if len(nvd_cve['vulnerabilities']) == 0 else True
            if self.is_valid != True:
                return
            vulnerabilities = next((x for x in nvd_cve['vulnerabilities']), None)
            if vulnerabilities:
                cve = vulnerabilities['cve']
                self.__id = cve['id']

                descriptions = next((x for x in cve['descriptions'] if x['lang'] == 'en'), None)
                self.__descriptions = descriptions['value']

                metrics = cve['metrics']
                cvssMetricV = next((x for x in metrics if 'cvssMetricV4' in x), None)
                if cvssMetricV is None:
                    cvssMetricV = next((x for x in metrics if 'cvssMetricV3' in x), None)
                    if cvssMetricV is None:
                        cvssMetricV = next((x for x in metrics if 'cvssMetricV2' in x), None)
                if cvssMetricV is not None:
                    cvssData = metrics[cvssMetricV][0]['cvssData']
                    self.__cvssMetric_version = cvssData['version']
                    self.__cvssMetric_score = cvssData['baseScore']
                    version = cvssData['version']

                if 'weaknesses' in cve:
                    weaknesses = cve['weaknesses']
                if 'configurations' in cve:
                    configurations = cve['configurations']
                if 'references' in cve:
                    references = cve['references']

    @property
    def is_valid(self):
        return self.__is_valid
    
    @property
    def id(self):
        return self.__id

    @property
    def cvssMetric_version(self):
        return self.__cvssMetric_version
    
    @property
    def cvssMetric_score(self):
        return self.__cvssMetric_score
    
    @property
    def descriptions(self):
        return self.__descriptions
        
    def toJson(self, outfile=None):
        if outfile is None:
            outfile = self.id + ".json"
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(self.__nvd_cve, f, indent=2)

    def dump(self):
        print("is_valid: ", self.is_valid)
        print("id: ", self.id)
        print("version: ", self.cvssMetric_version)
        print("score: ", self.cvssMetric_score)
        print("description: ", self.descriptions)
        print()
        
    def dump_nvd_cve(self):
        print(json.dumps(self.__nvd_cve, indent=2))

class NVDAPI(object):
    schema={
        "CVE API": 'https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema',
        "CVSSv3.1":'https://csrc.nist.gov/schema/nvd/api/2.0/external/cvss-v3.1.json',
        "CVSSv3.0": 'https://csrc.nist.gov/schema/nvd/api/2.0/external/cvss-v3.0.json',
        "CVSSv2.0": 'https://csrc.nist.gov/schema/nvd/api/2.0/external/cvss-v2.0.json',
        "CVE Change History API": 'https://csrc.nist.gov/schema/nvd/api/2.0/cve_history_api_json_2.0.schema'
    }
    api={
        "CVE API": 'https://services.nvd.nist.gov/rest/json/cves/2.0',
        "CVE Change History": 'https://services.nvd.nist.gov/rest/json/cvehistory/2.0'
    }
    param_cveId='cveId'
    param_pubStartDate='pubStartDate'
    param_pubEndDate='pubEndDate'
    param_totalResults='totalResults'
    param_resultsPerPage='resultsPerPage'
    param_startIndex='startIndex'
    param_changeStartDate='changeStartDate'
    param_changeEndDate='changeEndDate'

    def __init__(self, nvd_cve_dir="nvd.data0"):
        self.version = 2.0
        self.__nvd_cve_dir = Path(nvd_cve_dir)
        self.nvd_cve_dir.mkdir(exist_ok=True)

    def request_cve_api(self, params, delay=6):
        bbreak = False
        totalResults = 0
        receivedPage = 0
        pprint(params)
        while True:
            response = requests.get(self.CVE_API_20, params=params)
            if response.status_code != 200:
                print("request is failed.. ", response.status_code)
                bbreak = True
            else:
                nvd_cve = json.loads(response.text)
                print(json.dumps(nvd_cve, indent=2))
                totalResults = nvd_cve[self.param_totalResults]
                receivedPage += nvd_cve[self.param_resultsPerPage]
                if receivedPage < totalResults:
                    params[self.param_startIndex] = receivedPage
                else:
                    bbreak = True
                self.toJson(nvd_cve)

            time.sleep(delay)

            if bbreak:
                break
    
    def request_cveId(self, cve_id, exist_ok=False, delay=6):
        print("{0} ".format(cve_id), end='')
        cve = None
        if exist_ok:
            a= self.toPath(cve_id)
            if a.exists():
                print("is already exists")
                cve = NVDCVE()
                cve.load(a)
                return cve

        params = {self.param_cveId:cve_id}
        response = requests.get(self.api["CVE API"], params=params)
        if response.status_code != 200:
            print("request is failed.. ", response.status_code)
        else:
            nvd_cve = json.loads(response.text)
            cve = NVDCVE(nvd_cve)
            self.toJson(nvd_cve)

        time.sleep(delay)
        return cve

    def request_cve_update_history(self, params, delay=6):
        bbreak = False
        totalResults = 0
        receivedPage = 0
        while True:
            response = requests.get(self.api["CVE Change History"], params=params)
            if response.status_code != 200:
                print("request is failed.. ", response.status_code)
                bbreak = True
            else:
                nvd_cve = json.loads(response.text)
                # print(json.dumps(nvd_cve, indent=2))
                totalResults = nvd_cve[self.param_totalResults]
                receivedPage += nvd_cve[self.param_resultsPerPage]
                if receivedPage < totalResults:
                    params[self.param_startIndex] = receivedPage
                else:
                    bbreak = True
                self.toJson0(nvd_cve, self.makePath("cve.history"))

            time.sleep(delay)

            if bbreak:
                break

    def toJson0(self, nvd_cve, outfile):
        if outfile is None:
            return
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(nvd_cve, f, indent=2)

    def toJson(self, nvd_cve):
        if 'vulnerabilities' not in nvd_cve:
            print("invalid nvd_cve")
            return
        vulnerabilities = [x for x in nvd_cve['vulnerabilities']]
        for vulnerability in vulnerabilities:
            if 'cve' in vulnerability:
                cve = vulnerability['cve']
                cve_id = cve['id']
                if cve_id is not None:
                    cve_data = {'format': nvd_cve['format'],
                                'version': nvd_cve['version'],
                                'timestamp': nvd_cve['timestamp'],
                                'vulnerabilities': vulnerability}

                    with open(self.makePath(cve_id), 'w', encoding='utf-8') as f:
                        json.dump(json.loads(json.dumps(cve_data)), f, indent=2)

    def makePath(self, cve_id):
        return self.nvd_cve_dir / "{0}.json".format(cve_id)

    @property
    def nvd_cve_dir(self):
        return self.__nvd_cve_dir

if __name__ == '__main__':
    if False:
        nvdapi = NVDAPI()
        with open('a.json', 'r') as f:
            nvd_data = json.load(f)
            nvdapi.toJson(nvd_data)
        exit()

    if False:
        print(datetime.datetime.now())
        print(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")+"+09:00")
        print(datetime.datetime.now(tz=datetime.timezone.utc))
        print(datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z"))
        exit()
    if False:
        cve_id = "CVE-2024-56775"
        nvdapi = NVDAPI()
        # params = {NVDAPI.param_cveId :cve_id}
        params = {
            NVDAPI.param_pubStartDate:'2025-02-18T00:00:00+09:00',
            NVDAPI.param_pubEndDate:'2025-02-19T00:00:00+09:00',
            NVDAPI.param_resultsPerPage: 80,
            NVDAPI.param_startIndex:0
            }
        nvdapi.request_cve_api(params)
        exit()
    if False:
        nvdapi = NVDAPI("nvd.data5")
        params = {
            NVDAPI.param_changeStartDate: '2025-02-20T00:00:00+09:00',
            NVDAPI.param_changeEndDate:'2025-02-21T00:00:00+09:00'
            }
        nvdapi.request_cve_update_history(params)
        exit()
    if False:
        cve_id = "CVE-2024-56775"
        cve_id = "CVE-2022-28391"
        cve_id = "CVE-2007-4476"
        nvdapi = NVDAPI("nvd.data4")
        cve = nvdapi.request_cveId(cve_id, False, 0)
        cve.dump_nvd_cve()
        exit()
    if False:
        cve_id = "CVE-2017-0000"
        cve_id = "CVE-2024-56775"
        nvdapi = NVDAPI()
        cve = NVDCVE()
        cve.load(nvdapi.makePath(cve_id))
        cve.dump()
        cve.dump_nvd_cve()
        exit()
    if False:
        cve_id_list = list()
        with open('sample.short.csv', 'r') as f:
            rr = csv.reader(f, delimiter="\t")
            for line in rr:
                cve_id_list.append(line[1])
    
        cve_list = list()
        for cve_id in cve_id_list:
            nvdapi = NVDAPI('nvd.data4')
            cve = nvdapi.request_cveId(cve_id)

            if cve and cve.is_valid:
                xxx = next((x for x in cve_list if x.id == cve_id), None)
                if xxx:
                    continue
                cve_list.append(cve)

        print("cve_list: ", len(cve_list))
        exit()
    if False:
        cve_id_list = list()
        with open('sample.long.csv', 'r') as f:
            rr = csv.reader(f, delimiter="\t")
            for line in rr:
                cve_id_list.append(line[1])
    
        cve_list = list()
        for cve_id in cve_id_list:
            cve = NVDCVE()
            cve.load(NVDAPI.nvd_cve_dir / "{0}.json".format(cve_id))

            if cve and cve.is_valid:
                xxx = next((x for x in cve_list if x.id == cve_id), None)
                if xxx:
                    continue
                cve_list.append(cve)

        print("cve_list: ", len(cve_list))

        with open('cveto.csv', 'w', newline='', encoding='utf-8') as f:
            wr = csv.writer(f)
            for icve, cve in enumerate(cve_list):
                wr.writerow([icve, cve.id, cve.cvssMetric_score, cve.descriptions])
        exit()
