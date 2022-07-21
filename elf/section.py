import sys,os
from elftools.elf.elffile import ELFFile
from elftools.elf.segments import Segment
from elftools.elf.sections import Section, NullSection
import argparse

if __name__ == '__main__':
    efile0 = "libglib-2.0.so.0.7200.1.so"
    with open(efile0, 'rb') as efile1:
        elffile = ELFFile(efile1)
        dynamic= elffile.get_section_by_name('.dynamic')
        dynstr = elffile.get_section_by_name('.dynstr')

        tag_soname = next((x for x in dynamic.iter_tags() if x.entry['d_tag'] == 'DT_SONAME'), None)
        if tag_soname == None:
            exit(0)
        d_val = tag_soname.entry['d_val']
        print("    SONAME: {0}".format(dynstr.get_string(d_val)))
        
        tag_needed = [x for x in dynamic.iter_tags() if x.entry['d_tag'] == 'DT_NEEDED']
        if len(tag_needed) == 0:
            exit(0)

        for needed in tag_needed:
            d_val = needed.entry['d_val']
            print("      NEEDED: {0}".format(dynstr.get_string(d_val)))

        # print("sections: {0}".format(elffile.num_sections()))
        # for isection in range(elffile.num_sections()):
        #     section = elffile.get_section(isection)
        #     if section.is_null() == True:
        #         continue

        #     if section['sh_type'] == 'SHT_DYNAMIC':
        #         print("  tags: {0}".format(section.num_tags()))
        #         for itag in range(section.num_tags()):
        #             tag = section.get_tag(itag)
        #             # d_val = section.get_tag(itag).entry['d_val']
        #             # print("    {0}".format(dynstr.get_string(d_val)))
        #             print("    {0}".format(tag.entry['d_tag']))
                    
    print("done")

