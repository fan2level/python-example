# -*-coding:utf-8-*-

import os,sys
from pathlib import Path
import argparse
import re

default_match = set()
default_match.add('open')
default_match.add('read')
default_match.add('write')
default_match.add('ioctl')
default_match.add('close')
default_match.add('popen')
default_match.add('pclose')
default_match.add('memset')
default_match.add('memcpy')
default_match.add('strcpy')
default_match.add('strncpy')
default_match.add('system')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', required=True, help="target path")
    parser.add_argument('--match','-m', type=str, help="csv style string to match")
    args = parser.parse_args()

    target_root = args.path
    target_matches = None
    if args.match is None:
        target_matches = default_match
    else:
        target_matches = [x for x in args.match.split(',') if len(x) > 0]

    for root, sub, files in os.walk(os.path.abspath(target_root)):
        for file in files:
            if file.endswith(('.c')) == False and file.endswith(('.cpp')) == False:
                continue

            target_path = os.path.join(root, file)
            # print(target_path)
            with open(target_path, 'r', encoding='utf-8') as f:
                all_lines = list()
                try:
                    all_lines = f.readlines()
                except Exception as e:
                    print("exception, {0}: {1}".format(target_path, e))
                    
                for line in all_lines:
                    line = line.strip()
                    # [#1] 주석안에 작성된 경우
                    pattern0 = re.compile(r"(?P<line>.*)//.*")
                    m = pattern0.search(line)
                    if m:
                        line = m.group('line')
                    # [#1] 주석안에 작성된 경우
                    pattern1 = re.compile(r"(?P<line1>.*)(/\*.*\*/)(?P<line2>.*)")
                    m = pattern1.search(line)
                    if m:
                        line = m.group('line1') + m.group('line2')
                    # [#1] 주석안에 작성된 경우
                    pattern1 = re.compile(r"(?P<line1>.*)(\".*\")(?P<line2>.*)")
                    m = pattern1.search(line)
                    if m:
                        line = m.group('line1') + m.group('line2')
                    if len(line) > 0:
                        for match in target_matches:
                            # [#2] match 문자열만 필터링
                            pattern2 = re.compile(r"[^a-zA-Z]{0}\s*\(".format(match))
                            m = pattern2.search(line)
                            if m:
                                # [#3] 반환값이 사용된 경우 필터링
                                pattern4 = re.compile(r"[.:_=(({{]\s*{0}".format(match))
                                n = pattern4.search(line)
                                if n:
                                    continue
                                # [#4] 반환값이 사용된 경우 필터링
                                pattern5 = re.compile(r"return\s*{0}".format(match))
                                n = pattern5.search(line)
                                if n:
                                    continue
                                # [#5] 로그 api와 함께 사용된 경우
                                pattern9 = re.compile(r".*log.*".format(match), re.I)
                                n = pattern9.search(line)
                                if n:
                                    continue
                                print('{0}: {1}'.format(target_path, line))

    print('done')
