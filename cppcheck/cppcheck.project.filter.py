# -*-coding:utf-8-*-
# filter utility from compile_commands.json

import os,sys
import argparse
import json
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, help="compile_commands.json file")
    parser.add_argument('--output', '-o', required=True, help="output file")
    parser.add_argument('--filter', '-f', type=str, help="csv style include filter... regexp")
    parser.add_argument('--exclude', '-e', type=str, help="csv style exclue filter... regexp")
    parser.add_argument('--debug', '-d', action='store_true', help="print debug information")
    args = parser.parse_args()
    
    ifile = args.input
    ofile = args.output
    filter_includes = list()
    filter_excludes = list()
    debug = args.debug
    
    if args.filter:
        filter_includes = [x for x in args.filter.split(',') if len(x) > 0]
    pattern_includes = [re.compile(r".*\/{0}.*".format(x)) for x in filter_includes]
    if args.exclude:
        filter_excludes = [x for x in args.exclude.split(',') if len(x) > 0]
    pattern_excludes = [re.compile(r".*\/{0}.*".format(x)) for x in filter_excludes]

    if debug:
        print("include patterns: ", pattern_includes)
        print("exclude patterns: ", pattern_excludes)

    with open(ifile) as j:
        jj = json.load(j)

    jj2 = list() if pattern_includes else jj
    for elem in jj:
        x = next((x for x in pattern_includes if x.search(elem['directory'])), None)
        if x:
            jj2.append(elem)
        
    jj3 = list()
    for elem in jj2:
        x = next((x for x in pattern_excludes if x.search(elem['directory'])), None)
        if x:
            continue
        jj3.append(elem)

    with open(ofile, 'w') as j:
        json.dump(jj3, j, indent=4)

    print('done')
    if debug:
        [print(x['file']) for x in jj3]
        print('')
