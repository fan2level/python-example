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
        self.pathset = list()

    def walk_path(self, node, path, indent=0):
        ''' get AUTOSAR path to dictionary
        '''
        if node.tag == self.ns_+"SHORT-NAME":
            path['p'] = node.text
        else:
            # tag = node.tag.replace(self.ns_, '')
            # path['p'] = tag
            subpath = list()
            for child in node:
                childpath = dict()
                subpath.append(childpath)
                self.walk_path(child, childpath, indent+2)
            # path 없는 노드는 삭제
            if len(subpath) > 0:
                x0 = [x for x in subpath if len(x) == 0]
                if len(x0) > 0:
                    [subpath.remove(x) for x in x0]
                if len(subpath) > 0:
                    path['/'] = subpath

    def makepath0(self, path, pathset):
        ''' return path to pathset
        `pathset {'n':name, 'c':childlen, 'p':parent}
        '''
        x = next((x for x in path if 'p' in x), None)
        xn= [x for x in path if '/' in x]
        if x is not None:
            path = x['p']
            pathset['n'] = x['p']
        if len(xn) > 0:
            pathset_childlen = list()
            pathset['c'] = pathset_childlen
            for subpath in xn:
                pathset_child = {'p':pathset}
                pathset_childlen.append(pathset_child)
                self.makepath0(subpath['/'], pathset_child)
        return pathset

    def makepath1(self, pathset):
        if 'n' in pathset:
            path = self.getpath(pathset)
            path = re.sub('\/+','/',path)
            self.pathset.append(path)
        if 'c' in pathset:
            for child in pathset['c']:
                self.makepath1(child)
    
    def getpath(self, pathset):
        uri = ''
        if pathset is None:
            return uri
        if 'n' in pathset:
            uri+=pathset['n']
        uri = self.getpath(pathset['p'])+'/'+uri
        return uri
        
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
    
    # filepath = 'sample/AUTOSAR_MOD_AISpecification_BaseTypes_Standard.arxml'
    # filepath = 'b.arxml'
    filepath = 'c.xml'
    filepath = 'sample/AUTOSAR_MOD_ECUConfigurationParameters.arxml'
    # filepath = 'sample/AUTOSAR_MOD_AISpecification_Collection_Body_Blueprint.arxml'
    ar = Arxml(Path(filepath), ll)
    path = {'p':'/'}
    ar.walk_path(ar.root, path, 0)
    # pprint(path)
    ll.debug('======================================================================')
    pathset0 = {'p':None}
    ar.makepath0(path['/'], pathset0)
    ar.makepath1(pathset0)
    [ll.debug(x) for x in ar.pathset]
    ll.debug('done')
                        
