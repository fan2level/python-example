import sys,os
from elftools.elf.elffile import ELFFile
from elftools.elf.segments import Segment
import argparse

if __name__ == '__main__':
    efile = "libglib-2.0.so.0.7200.1"
    with open(efile, 'rb') as elffile:
        for segment in ELFFile(elffile).iter_segments():
            print(segment.header)

    print("done")

