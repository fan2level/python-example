# -*-coding:utf-8-*-

import os,sys
from pathlib import Path
from xml.etree.ElementTree import *
import logging
import collections
import re

class Arxml(object):
    ns = 'http://autosar.org/schema/r4.0'
    ns_= '{'+ ns + '}'
    p0 = re.compile('^.*-REF$')
    def __init__(self, arxml):
        self.__file = Path(arxml)
        tree = parse(arxml)
        root = tree.getroot()
        self.__root = root

    def walk_rucursive(self, node, indent=0):
        print(' '*indent+node.tag)
        indent+=2
        for node0 in node:
            self.walk_rucursive(node0, indent)

    def search_ref(self, node):
        if self.p0.search(node.tag) and 'DEST' in node.attrib:
            print(node.attrib['DEST'])
        for node0 in node:
            self.search_ref(node0)
        
    def ADMIN_DATA(self):
        pass
    def ECUC_DEFINITION_COLLECTIONS(self):
        pass
    def ECUC_MODULE_DEF(self):
        pass
    def ECUC_PARAM_CONF_CONTAINER_DEF(self):
        pass
        
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

if __name__=='__main__':
    ll = logging.getLogger(__name__)
    ll.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(''))
    ll.addHandler(console)

    ar = Arxml('AUTOSAR_MOD_ECUConfigurationParameters.arxml')
    # ar.walk_rucursive(ar.root)
    ar.search_ref(ar.root)
