# -*-coding:utf-8-*-
# check elf file dependency

import os,sys
import argparse
import json
from pELF import pELF

parser = argparse.ArgumentParser()
parser.add_argument('--path', '-p', required=True, help="path to check dependency")
parser.add_argument('--target', '-t', help="specify elf file to check dependency in path")

args = parser.parse_args()
_path = args.path
_target = args.target

elfs = list()
for folder, sub, files in os.walk(_path):
    for file in files:
        try:
            efile = pELF(os.path.join(folder, file))
        except Exception as e:
            continue
        if efile.is_elf == False:
            continue

        elfs.append(efile)

for elf in elfs:
    print(json.loads(elf.toJson()))

if _target != None:
    pass
