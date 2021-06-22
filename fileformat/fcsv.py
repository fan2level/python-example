# -*-coding:utf-8-*-

import os,sys
import csv
import re
import json

for folder, sub, files in os.walk('./'):
    for file in files:
        if file.endswith('.csv') == False:
            continue

        output = '{0}.json'.format(os.path.splitext(file)[0])
        
        with open(file, 'r') as x:
            r = csv.DictReader(x,
                               ['date','fund','company','ticker','cusip', 'shares','value','weight'])
            next(r)
            r = [x for x in r if re.match(u'\d{1,2}/\d{1,2}/\d{4}', x['date'])]
            # for l in r:
            #     print(l)
            with open(output, mode='w', encoding='utf-8-sig') as f:
                f.write(json.dumps(r, ensure_ascii=False, indent=2))

        
