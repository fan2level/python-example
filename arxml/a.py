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
        try:
            if node.text:
                print(' '*indent+node.tag.replace(self.ns_,'')+' '+node.text.strip())
            else:
                print(' '*indent+node.tag.replace(self.ns_,''))
        except UnicodeEncodeError:
            print(' '*indent+node.tag.replace(self.ns_,'')+' '+'#########################')
        indent+=2
        for node0 in sorted(node, key=lambda x: (x.tag, x.text)):
            self.walk_rucursive(node0, indent)

    def search_ref(self, node):
        if self.p0.search(node.tag) and 'DEST' in node.attrib:
            print(node.attrib['DEST'])
        for node0 in node:
            self.search_ref(node0)

    def text(self, node, xpath):
        child = node.find(self.make_ns(xpath))
        if child is not None:
            return child.text
        return ''
    
    def AR_PACKAGES(self, node, indent=0):
        print(' '*indent+str(node.tag))
        indent+=2
        for child in sorted(node.findall(self.make_ns("AR-PACKAGE")), key=lambda x: self.text(x, 'SHORT-NAME')):
            self.AR_PACKAGE(child, indent+2)

    def AR_PACKAGE(self, node, indent=0):
        print(' '*indent+str(node.tag))
        print(' '*indent+self.text(node, 'SHORT-NAME'))
        indent+=2
        for child in node.findall(self.make_ns("AR-PACKAGES")):
            self.AR_PACKAGES(child, indent+2)
        
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
    ar.walk_rucursive(ar.root)
    # ar = Arxml('a.xml')
    # node = ar.root.find(ar.make_ns('AR-PACKAGES'))
    # ar.AR_PACKAGES(node, 0)
    # for node in ar.root:
    #     ll.debug(node)
    #     for node0 in node:
    #         ll.debug('  '+node0.tag)
    #         for node1 in node0:
    #             ll.debug('    '+node1.tag)
    #             for node2 in node1:
    #                 ll.debug('      '+node2.tag)
    #                 for node3 in node2:
    #                     ll.debug('        '+node3.tag)
        
    # node = ar.root.find(ar.make_ns(['AR-PACKAGES', 'AR-PACKAGE','AR-PACKAGES','AR-PACKAGE', 'SHORT-NAME']))
    # ll.debug(node.text)
                        
