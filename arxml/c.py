# -*-coding:utf-8-*-

import os,sys
import logging
from pathlib import Path
import argparse
from xml.etree.ElementTree import *
import re
from pprint import pprint

class Arxml(object):
    ns = 'http://autosar.org/schema/r4.0'
    ns_= '{'+ ns + '}'

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
            path['m'] = node.text.strip()
        else:
            # tag = node.tag.replace(self.ns_, '')
            # path['m'] = tag
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

    def makepath(self, node):
        ''' return unique pathset to list
        '''
        pathsetx = list()
        def makepath0(path, pathset):
            x = next((x for x in path if 'm' in x), None)
            xn= [x for x in path if '/' in x]
            if x is not None:
                path = x['m']
                pathset['n'] = x['m']
            if len(xn) > 0:
                pathset_childlen = list()
                pathset['c'] = pathset_childlen
                for subpath in xn:
                    pathset_child = {'p':pathset}
                    pathset_childlen.append(pathset_child)
                    makepath0(subpath['/'], pathset_child)
            return pathset
        def makepath1(pathset):
            if 'n' in pathset:
                path = getpath(pathset)
                path = re.sub('\/+','/',path)
                pathsetx.append(path)
            if 'c' in pathset:
                for child in pathset['c']:
                    makepath1(child)

        def getpath(pathset):
            uri = ''
            if pathset is None:
                return uri
            if 'n' in pathset:
                uri+=pathset['n']
            uri = getpath(pathset['p'])+'/'+uri
            return uri

        path = {'m':'/'}
        self.walk_path(node, path)
        pathset0 = {'p':None}
        makepath0(path['/'], pathset0)
        makepath1(pathset0)
        return pathsetx
                    
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

    # parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument('--directory', '-d', help="directory path")
    # group.add_argument('--filepath', '-f', help="file path")
    # args = parser.parse_args()

    # a_directory = args.directory
    # a_filepath = args.filepath

    # if a_directory:
    #     for file in os.listdir(a_directory):
    #         filepath = Path(a_directory) / file
    #         ar = Arxml(filepath, ll)
    #         [ll.debug(x) for x in ar.makepath(ar.root)]
    # elif a_filepath:
    #     if Path(a_filepath).exists():
    #         filepath = a_filepath
    #         ar = Arxml(Path(filepath), ll)
    #         [ll.debug(x) for x in ar.makepath(ar.root)]
    
    # filepath = 'sample/AUTOSAR_MOD_AISpecification_BaseTypes_Standard.arxml'
    # filepath = 'b.arxml'
    filepath = 'c.xml'
    # filepath = 'sample/AUTOSAR_MOD_ECUConfigurationParameters.arxml'
    # filepath = 'sample/AUTOSAR_MOD_AISpecification_Collection_Body_Blueprint.arxml'
    ar = Arxml(Path(filepath), ll)
    [ll.debug(x) for x in ar.makepath(ar.root)]

    
    ll.debug('done')
                        
