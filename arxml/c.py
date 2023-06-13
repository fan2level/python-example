# -*-coding:utf-8-*-

import os,sys
import argparse
from pathlib import Path
from xml.etree.ElementTree import *
import logging
import re
from pprint import pprint

class Arxml(object):
    ns = 'http://autosar.org/schema/r4.0'
    ns_= '{'+ ns + '}'
    p0 = re.compile('^.*-REF$')
    def __init__(self, arxml, logger=logging):
        self.__file = Path(arxml)
        tree = parse(arxml)
        root = tree.getroot()
        self.__root = root
        self.__logger = logger

    def walk_path(self, node, path, indent=0):
        if node.tag == self.ns_+"SHORT-NAME":
            # ll.debug(' '*indent+node.text)
            path['name'] = node.text
        else:
            path['name'] = '_'
            subpath = list()
            path['/'] = subpath
            for child in node:
                subitem = dict()
                subpath.append(subitem)
                self.walk_path(child, subitem, indent+2)

    def make_ns(self, xpath):
        if isinstance(xpath, list):
            path = './'
            for xpath0 in xpath:
                path+='/'+self.ns_+xpath0
            return path
        else:
            return './'+self.ns_+xpath
        
    @property
    def file(self):
        return self.__file
    @property
    def root(self):
        return self.__root
    @property
    def logger(self):
        return self.__logger

if __name__=='__main__':
    ll = logging.getLogger(__name__)
    ll.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(''))
    ll.addHandler(console)
    
    filepath = 'sample/AUTOSAR_MOD_AISpecification_BaseTypes_Standard.arxml'
    # filepath = 'sample/AUTOSAR_MOD_ECUConfigurationParameters.arxml'
    filepath = 'c.xml'
    # filepath = 'b.arxml'
    ar = Arxml(Path(filepath), ll)
    path = {}
    ar.walk_path(ar.root, path, 0)
    pprint(path)
    
    print('done')
                        
