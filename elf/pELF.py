import sys,os
import json
from elftools.elf.elffile import ELFFile
from elftools.elf.segments import Segment
from elftools.elf.sections import Section, NullSection

class pELF(object):
    """
    parse elf for check dependency
    
    """
    def __init__(self, path):
        self.__pp = dict()
        self.__pp['path'] = os.path.abspath(path)
        self.__pp['link'] = os.path.realpath(path)
        ppelf = dict()
        self.__pp['elf'] = ppelf
        ppelf['name'] = 'none'
        self.__dep = list()
        ppelf['needed'] = list()
        self.is_elf = True
        with open(path, 'rb') as ef:
            efile = ELFFile(ef)
            e_type = efile.structs.e_type
            if e_type == 'ET_EXEC':
                ppelf['name'] = os.path.basename(path)
            elif e_type == 'ET_DYN':
                xx = next((x for x in efile.iter_segments() if x.header.p_type == 'PT_INTERP'), None)
                if xx != None:
                    ppelf['name'] = os.path.basename(path)
            else:
                self.is_elf = False
                print("e_type:{0} {1}".format(e_type), path)
                return
            dynamic= efile.get_section_by_name('.dynamic')
            dynstr = efile.get_section_by_name('.dynstr')

            tag_soname = next((x for x in dynamic.iter_tags() if x.entry['d_tag'] == 'DT_SONAME'), None)
            if tag_soname != None:
                d_val = tag_soname.entry['d_val']
                ppelf['name'] = dynstr.get_string(d_val)
            tag_needed = [x for x in dynamic.iter_tags() if x.entry['d_tag'] == 'DT_NEEDED']
            if len(tag_needed) != 0:
                for needed in tag_needed:
                    d_val = needed.entry['d_val']
                    ppelf['needed'].append(dynstr.get_string(d_val))
            if len(ppelf['needed']) == 0:
                del ppelf['needed']
        
    def __str__(self):
        return toJson()['elf']['name']

    def toJson(self):
        return json.dumps(self.__pp, ensure_ascii=False, indent=2)

    def dump(self):
        print(self.toJson())

if __name__ == '__main__':
    ii = '.sample/libglib-2.0.so'
    a = pELF(ii)
    a.dump()

    print('done')
